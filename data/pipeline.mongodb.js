// Pipeline MongoDB script for ETL process from raw JSON to normalized database.
// Database: gearvn_normalized

use('gearvn_normalized');

const fs = require('fs');

// Path to raw JSON data
const rawDataPath = './data/output/products_with_specs.json';

console.log("Loading raw data from " + rawDataPath);
const rawDataString = fs.readFileSync(rawDataPath, 'utf-8');

// Parse JSON Lines (JSONL)
const rawData = [];
for (let line of rawDataString.split(/\r?\n/)) {
    if (line.trim()) {
        try {
            rawData.push(JSON.parse(line));
        } catch (e) {
            console.error("Error parsing line:", e.message);
        }
    }
}

// Helpers
function slugify(text) {
    if (!text) return '';
    return text.toString().toLowerCase()
        .replace(/[àáạảãâầấậẩẫăằắặẳẵ]/g, "a")
        .replace(/[èéẹẻẽêềếệểễ]/g, "e")
        .replace(/[ìíịỉĩ]/g, "i")
        .replace(/[òóọỏõôồốộổỗơờớợởỡ]/g, "o")
        .replace(/[ùúụủũưừứựửữ]/g, "u")
        .replace(/[ỳýỵỷỹ]/g, "y")
        .replace(/đ/g, "d")
        .replace(/[^a-z0-9\s-]/g, "")
        .replace(/[\s_-]+/g, "-")
        .replace(/^-+|-+$/g, "");
}

function toSnakeCase(name) {
    if (!name) return "";
    return name.replace(/[^a-zA-Z0-9]/g, " ")
               .split(/\s+/)
               .filter(w => w.length > 0)
               .map(w => w.toLowerCase())
               .join("_");
}

function stripHtml(html) {
    if (!html) return '';
    return html.replace(/<[^>]*>?/gm, '');
}

function parsePrice(priceRaw) {
    if (!priceRaw) return null;
    let str = String(priceRaw);
    let match = str.match(/NumberInt\('?(\d+)'?\)/);
    if (match) {
        return parseFloat(match[1]);
    }
    let parsed = parseFloat(str.replace(/[^\d.-]/g, ''));
    return isNaN(parsed) ? null : parsed;
}

function normalizeUrl(url) {
    if (!url) return url;
    return url.replace("https: //", "https://").trim();
}

function isValidUrl(url) {
    return url && url.startsWith("https://");
}

let stats = {
    skipped: 0,
    brandsInserted: 0,
    brandsFound: 0,
    categoriesInserted: 0,
    categoriesFound: 0,
    productsInserted: 0,
    productsUpdated: 0,
    slugConflicts: 0
};

const brandCache = {};
const categoryCache = {};

function getOrCreateBrand(brandName, parentBrandId = null) {
    if (!brandName) return null;
    let key = brandName.trim().toLowerCase();
    
    if (brandCache[key]) {
        stats.brandsFound++;
        return brandCache[key];
    }

    let existing = db.brands.findOne({ name: { $regex: new RegExp("^" + brandName.trim() + "$", "i") } });
    if (existing) {
        let idStr = existing._id.toString();
        brandCache[key] = idStr;
        stats.brandsFound++;
        return idStr;
    }

    let newBrand = {
        name: brandName.trim(),
        slug: toSnakeCase(brandName.trim()),
        parentBrandId: parentBrandId,
        logoUrl: "",
        active: true,
        createdAt: new Date(),
        updatedAt: new Date()
    };
    
    let res = db.brands.insertOne(newBrand);
    let idStr = res.insertedId.toString();
    brandCache[key] = idStr;
    stats.brandsInserted++;
    return idStr;
}

function resolveBrand(rawBrand) {
    if (!rawBrand) return null;
    let parts = rawBrand.split(" / ");
    if (parts.length > 1) {
        let parentName = parts[0].trim();
        let childName = parts[1].trim();
        let parentId = getOrCreateBrand(parentName, null);
        return getOrCreateBrand(childName, parentId);
    } else {
        return getOrCreateBrand(rawBrand, null);
    }
}

function getOrCreateCategory(catName, parentId = null) {
    if (!catName) return null;
    let key = catName.trim().toLowerCase();
    
    if (categoryCache[key]) {
        stats.categoriesFound++;
        return categoryCache[key];
    }

    let existing = db.categories.findOne({ name: { $regex: new RegExp("^" + catName.trim() + "$", "i") } });
    if (existing) {
        let idStr = existing._id.toString();
        categoryCache[key] = idStr;
        stats.categoriesFound++;
        return idStr;
    }

    let newCat = {
        name: catName.trim(),
        slug: slugify(catName.trim()),
        description: "",
        parentId: parentId,
        imageUrl: "",
        sortOrder: 0,
        active: true,
        createdAt: new Date(),
        updatedAt: new Date()
    };
    
    let res = db.categories.insertOne(newCat);
    let idStr = res.insertedId.toString();
    categoryCache[key] = idStr;
    stats.categoriesInserted++;
    return idStr;
}

function resolveCategory(rawCategory, rawSubCategory) {
    if (!rawCategory) return null;
    let catId = getOrCreateCategory(rawCategory, null);
    if (rawSubCategory) {
        let subCatId = getOrCreateCategory(rawSubCategory, catId);
        return subCatId;
    }
    return catId;
}

console.log("Processing records...");

// Clean up potential conflicting index from previous runs
try { db.products.dropIndex("slug_1"); } catch (e) {}

// Basic index before loop for faster lookups
db.products.createIndex({ "metadata.externalId": 1, "metadata.source": 1 });
db.products.createIndex({ slug: 1 }, { unique: true });

for (let raw of rawData) {
    // 1. Validate & clean
    if (!raw.name || !raw.price || !raw.category || !raw.brand || !raw.images || raw.images.length === 0) {
        stats.skipped++;
        // console.log(`[Validate] Skipped record: ${raw.id} (missing required fields)`);
        continue;
    }

    let images = raw.images.map(normalizeUrl).filter(isValidUrl);
    if (images.length === 0) {
        stats.skipped++;
        // console.log(`[Validate] Skipped record: ${raw.id} (no valid images)`);
        continue;
    }

    // 2. Resolve Brand
    let brandId = resolveBrand(raw.brand);

    // 3. Resolve Category
    let categoryId = resolveCategory(raw.category, raw.sub_category);

    // 4. Transform -> Product model
    let baseSlug = slugify(raw.name);
    let finalSlug = baseSlug;
    
    let metadata = {
        source: "gearvn",
        externalId: raw.id,
        sourceUrl: normalizeUrl(raw.url)
    };

    let existingProduct = db.products.findOne({
        "metadata.source": metadata.source,
        "metadata.externalId": metadata.externalId
    });

    let product = {
        name: raw.name,
        slug: finalSlug,
        description: stripHtml(raw.description_html),
        descriptionHtml: raw.description_html,
        price: parsePrice(raw.price),
        compareAtPrice: null,
        sku: raw.id,
        thumbnail: normalizeUrl(raw.thumbnail),
        images: images,
        categoryId: categoryId,
        brandId: brandId,
        specs: raw.specs || {},
        tags: [],
        attributes: {},
        metadata: metadata,
        active: true,
        updatedAt: new Date()
    };

    if (!existingProduct) {
        product.createdAt = new Date();
    } else {
        product.createdAt = existingProduct.createdAt;
    }

    // Slug conflict resolution
    let slugSuffix = 2;
    while (true) {
        let slugExists = db.products.findOne({ slug: finalSlug });
        if (slugExists && (!existingProduct || slugExists._id.toString() !== existingProduct._id.toString())) {
            finalSlug = `${baseSlug}-${slugSuffix}`;
            slugSuffix++;
            stats.slugConflicts++;
        } else {
            break;
        }
    }
    product.slug = finalSlug;

    // 5. Upsert
    let filter = {
        "metadata.source": metadata.source,
        "metadata.externalId": metadata.externalId
    };

    let upsertResult = db.products.replaceOne(filter, product, { upsert: true });
    
    if (upsertResult.upsertedCount > 0 || upsertResult.upsertedId) {
        stats.productsInserted++;
    } else if (upsertResult.modifiedCount > 0) {
        stats.productsUpdated++;
    }
}

// 6. Post-process (Indexes)
console.log("Creating indexes...");
try { db.products.dropIndex("name_text_description_text_sku_text"); } catch (e) {}
db.products.createIndex({ name: "text", description: "text", sku: "text" });
db.products.createIndex({ categoryId: 1, active: 1 });
db.products.createIndex({ brandId: 1, active: 1 });
// slug index is already created as unique before the loop

console.log(`[Pipeline] Start — source: gearvn, total records: ${rawData.length}`);
console.log(`[Validate] Skipped: ${stats.skipped} records`);
console.log(`[Brand]    Inserted: ${stats.brandsInserted} | Found existing: ${stats.brandsFound}`);
console.log(`[Category] Inserted: ${stats.categoriesInserted} | Found existing: ${stats.categoriesFound}`);
console.log(`[Product]  Inserted: ${stats.productsInserted} | Updated: ${stats.productsUpdated}`);
console.log(`[Slug]     Conflicts resolved: ${stats.slugConflicts}`);
console.log("[Done]");
