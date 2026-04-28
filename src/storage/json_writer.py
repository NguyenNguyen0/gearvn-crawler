import json
from pathlib import Path
from utils.logger import logger


def save_products(products, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    data = [p.model_dump() for p in products]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logger.info(f"Saved {len(data)} products into {path}")
