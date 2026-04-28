from crawlers.base_crawler import BaseCrawler


class ListCrawler(BaseCrawler):
    async def fetch_category(self, url: str):
        html = await self.get_html(url)
        return html
