import requests
from typing import Optional


def fetch(url: str, timeout: int = 10) -> Optional[str]: 

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text

    except requests.RequestException as e:
        print(f"[fetch] Failed to fetch {url}: {e}")
        return None
