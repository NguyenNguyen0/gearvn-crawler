
import json
import uuid
import re
from datetime import datetime, timezone
import os

def to_snake_case(name):
    name = re.sub(r"[^a-zA-Z0-9]", " ", name)
    words = name.split()
    return "_".join([w.lower() for w in words])

input_file = "d:/WorkSpace/python/gearvn-crawler/data/input/gearvn_categories.json"
output_file = "d:/WorkSpace/python/gearvn-crawler/data/output/brands.json"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)[0]

brands_set = set()

for main_cat_name, sub_items in data.items():
    for item in sub_items:
        for key, value in item.items():
            for brand_dict in value:
                for brand_name, url in brand_dict.items():
                    brands_set.add(brand_name)

brands_list = []
for b in sorted(list(brands_set)):
    brand_id = str(uuid.uuid4())
    b_slug = to_snake_case(b)
    brand_obj = {
        "id": brand_id,
        "name": b,
        "slug": b_slug,
        "logoUrl": "",
        "active": True,
        "createdAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "updatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }
    brands_list.append(brand_obj)

os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(brands_list, f, indent=4, ensure_ascii=False)

print(f"Created {len(brands_list)} unique brands in {output_file}")

