import asyncio
from tqdm import tqdm

from loaders.category_loader import load_categories
from crawlers.list_crawler import ListCrawler
from crawlers.detail_crawler import DetailCrawler

from parsers.list_parser import parse_list
from parsers.detail_parser import parse_detail

from models.product_model import Product
from storage.json_writer import save_products


OUTPUT_PATH = "data/output/products.json"


async def main():
    categories = load_categories("data/input/gearvn_categories.json")

    list_crawler = ListCrawler()
    detail_crawler = DetailCrawler()

    await list_crawler.start()

    all_products = []
    seen_ids = set()

    try:
        for cat in categories:
            html = await list_crawler.fetch_category(cat["url"])
            products = parse_list(html)

            for p in tqdm(products, desc=f"{cat['brand']}"):
                if p["id"] in seen_ids:
                    continue

                seen_ids.add(p["id"])

                try:
                    detail_html = detail_crawler.get_html(p["url"])
                    detail_data = parse_detail(detail_html)

                    product = Product(
                        id=p["id"],
                        name=p["name"],
                        price=p["price"],
                        url=p["url"],
                        thumbnail=p["thumbnail"],
                        category=cat["category"],
                        sub_category=cat["sub_category"],
                        brand=cat["brand"],
                        images=detail_data["images"],
                        description_html=detail_data["description_html"],
                    )

                    product.merge_specs(
                        p.get("specs", {}), detail_data.get("specs_detail", {})
                    )

                    all_products.append(product)

                except Exception as e:
                    print(f"Detail error: {p['url']} - {e}")

    finally:
        await list_crawler.stop()

    save_products(all_products, OUTPUT_PATH)


if __name__ == "__main__":
    asyncio.run(main())
