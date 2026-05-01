// Import data from json to mongodb
function importJSON(path, collectionName) {
    const fs = require('fs');
    const data = JSON.parse(fs.readFileSync(path, 'utf-8'));
    db[collectionName].insertMany(data);
}

// Switch to the target database
use('products');

// Optional: Drop existing collections if you want a clean import
db.brands.drop();
db.categories.drop();

// Import the data
importJSON('./data/output/brands.json', 'brands');
importJSON('./data/output/categories.json', 'categories');

// Output the counts to verify
console.log('Brands count:', db.brands.countDocuments());
console.log('Categories count:', db.categories.countDocuments());

// View some sample data
db.brands.find().limit(2);
db.categories.find().limit(2);
