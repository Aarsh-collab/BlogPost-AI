import re
from bs4 import BeautifulSoup
from readability import Document

def clean(html_text: str) -> str:
    # Remove NULL bytes and invalid control characters
    safe_html = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", html_text)

    try:
        # Try readability first (best extraction)
        doc = Document(safe_html)
        html = doc.summary()
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator=" ", strip=True)

    except Exception:
        # Fallback: raw BeautifulSoup extraction (never crashes)
        soup = BeautifulSoup(safe_html, "html.parser")
        text = soup.get_text(separator=" ", strip=True)

    return text