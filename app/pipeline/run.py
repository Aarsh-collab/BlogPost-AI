from app.llms.research_planner import research_planner
from app.llms.style_controller import style_summarizer
from app.llms.summarizer import summarizer
from app.llms.writer import writer
from app.research.clean import clean
from app.research.search import search
from app.research.fetch import fetch
from app.utils.image_renderer import render_blog
from app.utils.validate_images import validate_images


def run_pipeline(user_prompt: str, user_images: list[dict]) -> str:

    research_scope = research_planner(user_prompt)

    search_queries = research_scope.get("search_queries", [])[:2]

    all_urls: list[str] = []
    for query in search_queries:
        all_urls.extend(search(query, 2))

    summaries = []
    for url in all_urls:
        html = fetch(url)
        if html is None:
            continue

        text = clean(html)

        try:
            summaries.append(summarizer(text))
        except Exception:
            continue

    style_spec = style_summarizer(user_prompt)

    blog = writer(summaries, user_prompt, style_spec, user_images)

    if user_images:
        validate_images(blog, user_images)

    return render_blog(blog, user_images)