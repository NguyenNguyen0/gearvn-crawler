use('nexatech_products');

const fs = require('fs');

const reviveMongoTypes = (obj) => {
    if (Array.isArray(obj)) {
        return obj.map(reviveMongoTypes);
    }

    if (obj && typeof obj === 'object') {
        if ('$oid' in obj) {
            return ObjectId(obj.$oid);
        }

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

const sourcePath = './data/output/miss_subcategories.json';
const documents = readJSONL(sourcePath);

if (!documents.length) {
    console.log('No documents found in miss_subcategories.json');
} else {
    const operations = documents.map((doc) => ({
        updateOne: {
            filter: {
                name: doc.name,
                parentId: doc.parentId
            },
            update: {
                $setOnInsert: doc
            },
            upsert: true
        }
    }));

    const result = db.getCollection('categories').bulkWrite(operations, { ordered: false });

    console.log(`Source documents: ${documents.length}`);
    console.log(`Inserted: ${result.upsertedCount}`);
    console.log(`Skipped existing: ${documents.length - result.upsertedCount}`);
}
