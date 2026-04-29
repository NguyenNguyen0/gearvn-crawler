import random

HEADLESS = True

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
]

HEADERS = {
    "User-Agent": random.choice(USER_AGENTS),
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def get_random_user_agent() -> str:
    return random.choice(USER_AGENTS)


# Playwright timeout (ms)
REQUEST_TIMEOUT = 30_000

# aiohttp timeout (giây)
REQUEST_TIMEOUT_SECONDS = 30

# Số category Playwright chạy song song (= số page trong pool)
CATEGORY_CONCURRENCY = 2

# Số request detail aiohttp chạy song song
DETAIL_CONCURRENCY = 32

DELAY_RANGE = (1, 3)
