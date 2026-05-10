use('nexatech_products');

const fs = require('fs');

const reviveMongoTypes = (obj) => {
    if (Array.isArray(obj)) {
        return obj.map(reviveMongoTypes);
    }

    if (obj && typeof obj === 'object') {

        // Convert ObjectId
        if ('$oid' in obj) {
            return ObjectId(obj.$oid);
        }

        // Convert Date
        if ('$date' in obj) {
            return new Date(obj.$date);
        }

        for (const key in obj) {
            obj[key] = reviveMongoTypes(obj[key]);
        }
    }

    return obj;
};

const readJSONL = (path) => {
    const rawData = fs.readFileSync(path, 'utf-8');

    return rawData
        .split(/\r?\n/)
        .filter(line => line.trim())
        .map(line => reviveMongoTypes(JSON.parse(line)));
};

const brands = readJSONL('./data/output/brands_normalized.json');
const categories = readJSONL('./data/output/categories_normalized.json');
const products = readJSONL('./data/output/products_normalized.json');

db.getCollection('brands').deleteMany({});
db.getCollection('categories').deleteMany({});
db.getCollection('products').deleteMany({});

if (brands.length) {
    db.getCollection('brands').insertMany(brands);
}

if (categories.length) {
    db.getCollection('categories').insertMany(categories);
}

if (products.length) {
    db.getCollection('products').insertMany(products);
}

console.log(`Imported ${brands.length} brands`);
console.log(`Imported ${categories.length} categories`);
console.log(`Imported ${products.length} products`);