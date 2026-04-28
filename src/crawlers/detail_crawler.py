import requests
from tenacity import retry, stop_after_attempt, wait_random

HEADERS = {"User-Agent": "Mozilla/5.0"}


class DetailCrawler:
    @retry(stop=stop_after_attempt(3), wait=wait_random(1, 3))
    def get_html(self, url: str):
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        return res.text
