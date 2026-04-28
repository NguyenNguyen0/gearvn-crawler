from typing import List, Dict, Optional
from pydantic import BaseModel


def normalize_key(key: str) -> str:
    return key.lower().replace(" ", "_").replace("-", "_").replace("/", "_")


class Product(BaseModel):
    id: str
    name: str
    price: Optional[int]

    url: Optional[str]
    thumbnail: Optional[str]

    category: Optional[str]
    sub_category: Optional[str]
    brand: Optional[str]

    images: List[str] = []
    specs: Dict[str, str] = {}

    description_html: Optional[str]

    def merge_specs(self, specs_list: dict, specs_detail: dict):
        merged = {}

        for k, v in {**specs_list, **specs_detail}.items():
            merged[normalize_key(k)] = v

        self.specs = merged
