use('nexatech_products');

const fs = require('fs');

const inputPath = './data/input/gearvn_categories.json';

const slugify = (text) => {
    return String(text)
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/-+/g, '-')
        .replace(/^-|-$/g, '');
};

const slugFromUrl = (url) => {
    try {
        const safeUrl = String(url || '');

        // mongosh may not reliably expose WHATWG URL in every runtime,
        // so parse path/query manually for compatibility.
        const noHash = safeUrl.split('#')[0];
        const [pathPart, queryPart = ''] = noHash.split('?');
        const pathSlug = (pathPart || '').replace(/\/+$/g, '').split('/').pop() || '';

        let hang = '';
        if (queryPart) {
            const pairs = queryPart.split('&');
            for (const pair of pairs) {
                const [k, v = ''] = pair.split('=');
                if (decodeURIComponent(k || '') === 'hang') {
                    hang = decodeURIComponent(v || '');
                    break;
                }
            }
        }

        if (hang) {
            const brandFromQuery = slugify(hang);
            if (brandFromQuery && !pathSlug.endsWith(`-${brandFromQuery}`)) {
                return slugify(`${pathSlug}-${brandFromQuery}`);
            }
        }

        return slugify(pathSlug);
    } catch (err) {
        return '';
    }
};

const loadBrandSlugs = (path) => {
    const raw = fs.readFileSync(path, 'utf-8');
    const data = JSON.parse(raw);

    // Input structure: [ { TopCategory: [ { brands: [...] } or { SubCategory: [...] } ] } ]
    const root = Array.isArray(data) && data.length ? data[0] : {};
    const slugs = new Set();

    for (const topCategoryName in root) {
        const items = root[topCategoryName] || [];

        for (const item of items) {
            for (const key in item) {
                const value = item[key];

                if (key === 'brands') {
                    for (const brandObj of value) {
                        for (const brandName in brandObj) {
                            const brandUrl = brandObj[brandName];
                            const slug = slugFromUrl(brandUrl);
                            if (slug) slugs.add(slug);
                        }
                    }
                } else {
                    // key is level-2 subcategory, value is brand list
                    for (const brandObj of value) {
                        for (const brandName in brandObj) {
                            const brandUrl = brandObj[brandName];
                            const slug = slugFromUrl(brandUrl);
                            if (slug) slugs.add(slug);
                        }
                    }
                }
            }
        }
    }

    return [...slugs];
};

const brandSlugs = loadBrandSlugs(inputPath);

if (!brandSlugs.length) {
    throw new Error('No brand slugs found from input file.');
}

console.log(`Found ${brandSlugs.length} unique brand slugs from input.`);

let matchedCount = 0;
let modifiedCount = 0;

for (const slug of brandSlugs) {
    const result = db.getCollection('categories').updateMany(
        { slug },
        {
            $set: {
                'filter.brandSlug': slug,
                metadata: {}
            }
        }
    );

    matchedCount += result.matchedCount;
    modifiedCount += result.modifiedCount;
}

console.log('Migration completed.');
console.log(`Matched brand categories: ${matchedCount}`);
console.log(`Modified documents: ${modifiedCount}`);
console.log(`Unmatched slugs: ${brandSlugs.length - matchedCount}`);
