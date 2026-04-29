import asyncio
from tqdm.asyncio import tqdm

from loaders.category_loader import load_categories
from crawlers.list_crawler import ListCrawler
from crawlers.detail_crawler import DetailCrawler

from parsers.list_parser import parse_list
from parsers.detail_parser import parse_detail

from models.product_model import Product
from storage.json_writer import save_products
from config.settings import CATEGORY_CONCURRENCY, DETAIL_CONCURRENCY
from utils.logger import logger


OUTPUT_PATH = "data/output/products.json"


async def fetch_product_detail(
    p: dict,
    cat: dict,
    detail_crawler: DetailCrawler,
) -> Product | None:
    """Crawl + parse detail 1 sản phẩm. Trả None nếu lỗi (không crash toàn bộ)."""
    try:
        detail_html = await detail_crawler.get_html(p["url"])
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
        product.merge_specs(p.get("specs", {}), detail_data.get("specs_detail", {}))
        return product

    except Exception as e:
        logger.warning(f"[detail] skip {p['url']} — {e}")
        return None


async def process_category(
    cat: dict,
    list_crawler: ListCrawler,
    detail_crawler: DetailCrawler,
    seen_ids: set,
    seen_lock: asyncio.Lock,
) -> list[Product]:
    """
    Crawl list + detail của 1 category.
    - list_crawler dùng Playwright (async, page pool)
    - detail_crawler dùng aiohttp (async, Semaphore)
    Trả list rỗng nếu toàn bộ category bị lỗi (không crash main).
    """
    try:
        html = await list_crawler.fetch_category(cat["url"])
    except Exception as e:
        logger.error(f"[list] skip category {cat.get('brand')} {cat['url']} — {e}")
        return []

    raw_products = parse_list(html)

    # Lọc duplicate — dùng lock vì nhiều category chạy đồng thời
    new_products: list[dict] = []
    async with seen_lock:
        for p in raw_products:
            if p["id"] not in seen_ids:
                seen_ids.add(p["id"])
                new_products.append(p)

    if not new_products:
        return []

    logger.info(f"[{cat['brand']}] {len(new_products)} sản phẩm mới → crawl detail...")

    tasks = [
        fetch_product_detail(p, cat, detail_crawler)
        for p in new_products
    ]

    results = await tqdm.gather(
        *tasks,
        desc=f"  {cat['brand']} ({len(new_products)})",
        leave=False,
    )

    return [r for r in results if r is not None]


async def main():
    categories = load_categories("data/input/gearvn_categories.json")
    logger.info(f"Loaded {len(categories)} categories")

    list_crawler = ListCrawler()
    detail_crawler = DetailCrawler(concurrency=DETAIL_CONCURRENCY)

    await list_crawler.start()
    await detail_crawler.start()

    all_products: list[Product] = []
    seen_ids: set[str] = set()
    seen_lock = asyncio.Lock()

    try:
        sem = asyncio.Semaphore(CATEGORY_CONCURRENCY)

        async def bounded_process(cat: dict) -> list[Product]:
            async with sem:
                # Bắt exception ngay tại đây → không bao giờ raise ra ngoài
                try:
                    return await process_category(
                        cat, list_crawler, detail_crawler, seen_ids, seen_lock
                    )
                except Exception as e:
                    logger.error(f"[bounded] unexpected error {cat.get('brand')}: {e}")
                    return []

        # Tạo tất cả task ngay, chạy song song theo Semaphore
        tasks = [asyncio.create_task(bounded_process(cat)) for cat in categories]

        # as_completed để update progress bar khi từng task xong
        for fut in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Categories"):
            products = await fut          # fut đã bắt exception bên trong, không raise
            all_products.extend(products)

    finally:
        # Đảm bảo tất cả task còn lại được cancel sạch trước khi close browser
        for t in tasks:
            if not t.done():
                t.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

        await list_crawler.stop()
        await detail_crawler.stop()

    logger.info(f"Total products crawled: {len(all_products)}")
    save_products(all_products, OUTPUT_PATH)


if __name__ == "__main__":
    import sys
    import warnings

    # Suppress known asyncio/Playwright unclosed transport warning on Windows
    if sys.platform == "win32":
        warnings.filterwarnings("ignore", category=ResourceWarning)
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
