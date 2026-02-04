from app.llms.research_planner import research_planner
from app.llms.summarizer import summarizer
from app.research.search import search
from app.research.fetch import fetch
from app.research.clean import clean
from app.llms.writer import writer
from app.llms.style_controller import style_summarizer
from app.utils.image_renderer import render_blog
from app.utils.validate_images import validate_images


def main():
    user_prompt = (
        "Write me a blog about my trip to Disney. "
        "Start from when I left and go backwards. "
        "My favorite ride was the Incredicoaster, "
        "while my kids loved Guardians of the Galaxy. "
        "I want a lot of emotions and vivid imagery of our excitement."
    )
    user_images = [
        {
            "image_id": "image_1",
            "caption": "Test image (opening emotional anchor)"
        }
    ]
    
# Research LLM called (research_planner.py)
    research_scope: dict = research_planner(user_prompt)

    print("\n=== RESEARCH SCOPE ===")
    print(research_scope)

# Start searching for URL's (search.py)
    search_queries = research_scope.get("search_queries", [])
    search_queries = search_queries[:2]

    all_urls: list[str] = []

    for query in search_queries:
        urls = search(query, 2)
        all_urls.extend(urls)


    print("\n=== SEARCH RESULTS (URLS) ===")
    print(all_urls)

# Fetch (fetch.py) -> clean (clean.py) -> summarize (summarizer.py)
    print("\n=== FETCH + CLEAN PREVIEW ===")

    summaries = []
    for url in all_urls:

        #fetch URL's htlm code

        html = fetch(url)
        if html is None:
            print("Fetch failed.")
            continue

        # clean text

        text = clean(html)

        #Summarizer text
        try:
            summary = summarizer(text)
            summaries.append(summary)
            print(summary["key_points"])
        except Exception as e:
            print("Summarizer Failed, skipping source")
            continue
        
    print("\n=== Blog Post ===")
    style_spec = style_summarizer(user_prompt)
    print(style_spec)
    blog = writer(summaries, user_prompt, style_spec, user_images)
    validate_images(blog, user_images)
    rendered = render_blog(blog, user_images)


    print(rendered)

if __name__ == "__main__":
    main()