
import json
import uuid
import re
from datetime import datetime
import os

def slugify(text):
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text

input_file = "d:/WorkSpace/python/gearvn-crawler/data/input/gearvn_categories.json"
output_file = "d:/WorkSpace/python/gearvn-crawler/data/output/categories.json"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)[0]

categories = []
sort_order = 1

def create_category(name, parent_id=None):
    global sort_order
    cat_id = str(uuid.uuid4())
    cat = {
        "id": cat_id,
        "name": name,
        "slug": slugify(name),
        "description": "Description for " + name,
        "parentId": parent_id,
        "imageUrl": "",
        "sortOrder": sort_order,
        "active": True,
        "createdAt": datetime.utcnow().isoformat() + "Z",
        "updatedAt": datetime.utcnow().isoformat() + "Z"
    }
    sort_order += 1
    categories.append(cat)
    return cat_id

for main_cat_name, sub_items in data.items():
    main_id = create_category(main_cat_name)
    
    for item in sub_items:
        for key, value in item.items():
            if key.lower() == "brands":
                # Ensure the name is specifically "Brands"
                brands_id = create_category("Brands", parent_id=main_id)
                for brand_dict in value:
                    for brand_name, url in brand_dict.items():
                        create_category(brand_name, parent_id=brands_id)
            else:
                sub_id = create_category(key, parent_id=main_id)
                brands_id = create_category("Brands", parent_id=sub_id)
                for brand_dict in value:
                    for brand_name, url in brand_dict.items():
                        create_category(brand_name, parent_id=brands_id)

os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(categories, f, indent=4, ensure_ascii=False)

print(f"Created {len(categories)} categories in {output_file}")

