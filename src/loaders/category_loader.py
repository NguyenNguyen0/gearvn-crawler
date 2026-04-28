import json
from pathlib import Path


def load_categories(path: str):
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return flatten_categories(data)


def flatten_categories(data):
    results = []

    for root in data:
        for category_name, category_value in root.items():
            for item in category_value:
                for key, value in item.items():
                    # CASE 1: "brands"
                    if key == "brands":
                        for brand_obj in value:
                            for brand, url in brand_obj.items():
                                results.append(
                                    {
                                        "category": category_name,
                                        "sub_category": None,
                                        "brand": brand,
                                        "url": url,
                                    }
                                )

                    # CASE 2: sub-category (PC Case, RAM,...)
                    else:
                        sub_category = key

                        for brand_obj in value:
                            for brand, url in brand_obj.items():
                                results.append(
                                    {
                                        "category": category_name,
                                        "sub_category": sub_category,
                                        "brand": brand,
                                        "url": url,
                                    }
                                )

    return results
