from ddgs import DDGS


def search(query: str, max_results: int = 5) -> list[str]:
    """
    Run a web search for a single query and return a flat list of result URLs.
    """
    urls: list[str] = []

    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)

        for result in results:
            href = result.get("href", None)
            if href:
                urls.append(href)

    return urls
