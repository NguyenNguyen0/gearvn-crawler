import asyncio
import aiohttp
from tenacity import AsyncRetrying, stop_after_attempt, wait_random

from config.settings import HEADERS, REQUEST_TIMEOUT_SECONDS


class DetailCrawler:
    """
    Async HTTP crawler dùng aiohttp — không cần browser.
    Semaphore giới hạn số request đồng thời.
    """

    def __init__(self, concurrency: int = 10):
        self._sem = asyncio.Semaphore(concurrency)
        self._session: aiohttp.ClientSession | None = None

    async def start(self):
        connector = aiohttp.TCPConnector(limit=0, ttl_dns_cache=300)
        timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT_SECONDS)
        self._session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=HEADERS,
        )

    async def stop(self):
        if self._session:
            await self._session.close()
            self._session = None

    async def get_html(self, url: str) -> str:
        async with self._sem:
            async for attempt in AsyncRetrying(
                stop=stop_after_attempt(3),
                wait=wait_random(1, 3),
                reraise=True,
            ):
                with attempt:
                    async with self._session.get(url) as resp:
                        resp.raise_for_status()
                        return await resp.text()
