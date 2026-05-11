use('nexatech_products');

// Danh sách các subcategory level 2 hợp lệ
const validLevel2Names = [
    'brands',
    'PC Case',
    'Power Supply (PSU)',
    'RAM',
    'SSD',
    'HDD',
    'Speakers',
    'Microphone',
    'Gaming Chair',
    'Ergonomic Chair'
];

// Lấy tất cả top-level categories (level 1)
const topLevelCategories = db.getCollection('categories').find({ parentId: null }).toArray();
const topLevelIds = topLevelCategories.map(c => c._id.toString());

console.log(`Found ${topLevelIds.length} top-level categories`);

// Với mỗi top-level category, tìm các children (level 2)
let deletedCount = 0;
for (const topId of topLevelIds) {
    const topLevel = db.getCollection('categories').findOne({ _id: ObjectId(topId) });
    
    // Tìm tất cả categories có parentId = topId
    const directChildren = db.getCollection('categories').find({ parentId: topId }).toArray();
    
    // Lọc ra những cái không phải valid level 2 (tức là brand names gắn trực tiếp vào level 1)
    const brandsToDelete = directChildren.filter(child => !validLevel2Names.includes(child.name));
    
    if (brandsToDelete.length > 0) {
        console.log(`\nTop-level: "${topLevel.name}" (${topId})`);
        console.log(`  Found ${brandsToDelete.length} invalid level 3 categories attached to level 1:`);
        
        for (const brand of brandsToDelete) {
            console.log(`    - Deleting: "${brand.name}" (${brand._id})`);
            db.getCollection('categories').deleteOne({ _id: brand._id });
            deletedCount++;
        }
    }
}

console.log(`\n✓ Total deleted: ${deletedCount} categories`);
