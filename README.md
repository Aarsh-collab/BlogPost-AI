**BlogPostAI** is an autonomous research-to-publication blog generation system.  
Given a single user prompt, it independently researches the topic, extracts key information, and writes a long-form blog post with a controllable narrative style — without human back-and-forth.

This is **not** a chat assistant.  
It is a **pipeline**.

---

## What This Project Does

From one prompt, BlogPostAI:

1. Plans research  
2. Searches the web  
3. Fetches and cleans sources  
4. Summarizes relevant information  
5. Extracts writing style  
6. Writes a complete blog post  
7. Renders the output in a UI  

All steps are automated.

---

## Core Architecture

User Prompt
↓
Research Planner (LLM)
↓
Search Engine
↓
Fetch HTML
↓
Clean Text
↓
Summarizer (LLM)
↓
Style Controller (LLM)
↓
Writer (LLM)
↓
Rendered Blog Output

Each stage is isolated and replaceable.

---

## Project Structure

app/
├── llms/
│   ├── research_planner.py     # Decides what to research
│   ├── summarizer.py           # Extracts key points from sources
│   ├── style_controller.py     # Infers tone, narrative style, audience
│   └── writer.py               # Writes the final blog post
│
├── research/
│   ├── search.py               # Runs search queries
│   ├── fetch.py                # Fetches raw HTML
│   └── clean.py                # Cleans text for LLMs
│
├── pipeline/
│   └── run.py                  # Orchestrates the full pipeline
│
├── utils/
│   ├── render_blog.py          # Converts text → displayable output
│   └── validate_images.py      # (Optional) image validation
│
└── ui/
└── streamlit.py            # Streamlit UI

---

## Key Design Decisions

### 1. Pipeline Over Chat
This system is **deterministic** and **one-shot**.  
No conversational memory. No backtracking.

---

### 2. LLMs Are Used Only Where They Add Value
LLMs are used for:
- Research planning
- Summarization
- Style inference
- Writing

Everything else is traditional code.

---

### 3. Style Is Decoupled From Writing
The writer does **not** decide tone or structure.  
Style is inferred once and passed in.

This prevents prompt drift and contradictions.

---

### 4. Strict JSON Output Was Intentionally Removed
Early versions enforced JSON outputs.

This was removed because:
- It caused frequent failures
- It added no real value for long-form writing
- Natural language output is more reliable for blogs

---

## What This Is Not

- ❌ A chatbot  
- ❌ A SEO keyword stuffer  
- ❌ A web scraper farm  
- ❌ A prompt-engineering toy  
- ❌ A Medium clone  

---

## Current Capabilities

- Reverse-chronological storytelling  
- First-person or third-person narration  
- Emotional or factual tone  
- Research-backed or experience-driven writing  
- Fully autonomous execution  
- UI-based execution via Streamlit  

---

## Known Limitations (Intentional)

- Scraping may fail on paywalled or protected sites (403s)
- Research depth depends on source availability
- No plagiarism detection
- No fact verification beyond retrieved sources

---

## How to Run

### Install dependencies
```bash
pip install -r requirements.txt

Run the Streamlit UI

streamlit run app/ui/streamlit.py


⸻

Example Prompt

Write me a blog about my trip to Disney.
Start from when I left and go backwards.
My favorite ride was the Incredicoaster,
while my kids loved Guardians of the Galaxy.
I want a lot of emotions and vivid imagery.

Output: a complete, styled blog post — no follow-ups required.

⸻

Project Status

MVP complete.

Further work would be:
	•	UX polish
	•	Export formats
	•	Caching
	•	Style presets

None are required for core functionality.

⸻

Why This Exists

This project explores autonomous content generation as a system — not as a chat trick.

Writing is treated as a pipeline problem, not a conversation.

⸻

License

MIT

---

If you want:
- a **short recruiter README**
- a **startup-style README**
- or a **1-page stripped version**

say the word.