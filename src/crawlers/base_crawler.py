from playwright.async_api import async_playwright
from config.settings import HEADLESS, get_random_user_agent, REQUEST_TIMEOUT
from utils.logger import logger


class BaseCrawler:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None

    async def start(self):
        self.pw = await async_playwright().start()

        self.browser = await self.pw.chromium.launch(headless=HEADLESS)

        self.context = await self.browser.new_context(
            user_agent=get_random_user_agent()
        )

        self.page = await self.context.new_page()

        logger.info("Browser started")

    async def stop(self):
        await self.browser.close()
        await self.pw.stop()
        logger.info("Browser stopped")

    async def get_html(self, url: str):
        logger.info(f"Fetching: {url}")

        await self.page.goto(url, timeout=REQUEST_TIMEOUT)

        # chờ network idle (JS load xong)
        await self.page.wait_for_load_state("networkidle")

        html = await self.page.content()

        return html
