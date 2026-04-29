from crawlers.base_crawler import BaseCrawler
from config.settings import CATEGORY_CONCURRENCY


class ListCrawler(BaseCrawler):
    """
    Crawler danh sách sản phẩm dùng Playwright page pool.
    Số page = CATEGORY_CONCURRENCY để hỗ trợ song song.
    """

    def __init__(self):
        super().__init__(max_pages=CATEGORY_CONCURRENCY)

    async def fetch_category(self, url: str) -> str:
        return await self.get_html(url)
