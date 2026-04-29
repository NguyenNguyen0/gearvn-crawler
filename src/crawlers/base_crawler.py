import asyncio
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from config.settings import HEADLESS, get_random_user_agent, REQUEST_TIMEOUT
from utils.logger import logger


class BaseCrawler:
    """
    Playwright browser crawler với page pool.
    - max_pages page được tạo sẵn khi start()
    - get_html() lấy 1 page từ pool, trả lại sau khi dùng
    - Nếu page bị crash, tự tạo page mới thay thế
    """

    def __init__(self, max_pages: int = 1):
        self.max_pages = max_pages
        self._pw = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page_pool: asyncio.Queue | None = None

    async def start(self):
        self._pw = await async_playwright().start()
        self._browser = await self._pw.chromium.launch(headless=HEADLESS)
        self._context = await self._browser.new_context(
            user_agent=get_random_user_agent(),
        )
        self._page_pool = asyncio.Queue()
        for _ in range(self.max_pages):
            page = await self._context.new_page()
            await self._page_pool.put(page)
        logger.info(f"Browser started — {self.max_pages} page(s) in pool")

    async def stop(self):
        for obj in (self._browser, self._pw):
            if obj:
                try:
                    await obj.close()
                except Exception:
                    pass
        logger.info("Browser stopped")

    async def get_html(self, url: str) -> str:
        page: Page = await self._page_pool.get()
        success = False
        try:
            logger.info(f"Fetching: {url}")
            await page.goto(url, timeout=REQUEST_TIMEOUT)
            await page.wait_for_load_state("networkidle")
            html = await page.content()
            success = True
            return html
        finally:
            if not success:
                # Page bị crash/closed — đóng và tạo mới thay thế
                try:
                    await page.close()
                except Exception:
                    pass
                try:
                    page = await self._context.new_page()
                    logger.debug("Replaced crashed page with a new one")
                except Exception as e:
                    logger.error(f"Could not create replacement page: {e}")
                    return  # pool giảm 1 nhưng không crash toàn bộ
            await self._page_pool.put(page)
