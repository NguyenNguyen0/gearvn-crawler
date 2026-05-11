import json
from pathlib import Path

path = Path(r'd:/WorkSpace/python/gearvn-crawler/data/output/miss_subcategories.json')
lines = [line.strip() for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]

# Filter 'brands' subcategories at level 2
brands_subs = [json.loads(line) for line in lines if json.loads(line)['name'] == 'brands']
print(f'brands subcategories found: {len(brands_subs)}')
for doc in brands_subs[:3]:
    print(f'  - name: {doc["name"]}, parentId: {doc["parentId"]}, slug: {doc["slug"]}')

# Check ASUS entries at level 3
sample_brands = [json.loads(line) for line in lines if json.loads(line)['name'] == 'ASUS']
print(f'\nASUS entries found: {len(sample_brands)}')
for doc in sample_brands[:3]:
    print(f'  - slug: {doc["slug"]}, parentId: {doc["parentId"]}')
