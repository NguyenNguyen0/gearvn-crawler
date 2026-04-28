import random

HEADLESS = True   

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
]


def get_random_user_agent():
    return random.choice(USER_AGENTS)


REQUEST_TIMEOUT = 30000  # ms

DELAY_RANGE = (1, 3)
