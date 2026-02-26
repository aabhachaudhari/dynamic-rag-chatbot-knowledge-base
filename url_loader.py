# url_loader.py

import os
import re
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

CONTENT_TAGS = ["p", "h1", "h2", "h3", "h4", "li"]
JUNK_TAGS = [
    "script", "style", "nav", "footer", "header",
    "aside", "form", "button", "svg", "img",
    "noscript", "iframe", "table", "sup"
]

WIKIPEDIA_STOP_SECTIONS = [
    "references", "further reading", "external links",
    "see also", "notes", "bibliography", "citations",
    "footnotes", "sources"
]

CACHE_DIR = "data/url_cache"


def url_to_label(url):
    url = url.replace("https://", "").replace("http://", "").replace("www.", "")
    return url.split("/")[0]


def url_to_cache_filename(url):
    safe = url.replace("https://", "").replace("http://", "")
    safe = safe.replace("/", "_").replace(":", "_").replace("?", "_")
    return os.path.join(CACHE_DIR, safe[:120] + ".txt")


def clean_text(text):
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'\[edit\]', '', text)
    text = re.sub(r'\[note \d+\]', '', text)
    text = re.sub(r'\[citation needed\]', '', text)
    text = re.sub(r'\{\\displaystyle[^}]*\}', '', text)
    text = re.sub(r'\{[^}]{0,200}\}', '', text)
    text = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', text)
    text = re.sub(r'[∈∑Σ∀∃→←⟨⟩≤≥≠≈∞∂∇]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def is_wikipedia(url):
    return "wikipedia.org" in url


def parse_wikipedia(html):
    soup = BeautifulSoup(html, "lxml")
    for tag in soup.find_all(JUNK_TAGS):
        tag.decompose()

    content_div = soup.find("div", {"id": "mw-content-text"})
    if not content_div:
        content_div = soup

    lines = []
    stop = False

    for tag in content_div.find_all(["p", "h2", "h3", "h4"]):
        if stop:
            break
        if tag.name in ["h2", "h3", "h4"]:
            heading_text = tag.get_text().strip().lower()
            heading_text = re.sub(r'\[.*?\]', '', heading_text).strip()
            if any(s in heading_text for s in WIKIPEDIA_STOP_SECTIONS):
                stop = True
                break
            continue
        text = tag.get_text(separator=" ", strip=True)
        text = clean_text(text)
        if len(text) > 40:
            lines.append(text)

    return "\n".join(lines)


def parse_general(html):
    soup = BeautifulSoup(html, "lxml")
    for tag in soup.find_all(JUNK_TAGS):
        tag.decompose()
    lines = []
    for tag in soup.find_all(CONTENT_TAGS):
        text = tag.get_text(separator=" ", strip=True)
        text = clean_text(text)
        if len(text) > 30:
            lines.append(text)
    return "\n".join(lines)


def fetch_url(url, timeout=20):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = url_to_cache_filename(url)
    source_label = url_to_label(url)

    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            text = f.read()
        if text.strip():
            print(f"    [cache] {source_label}")
            return text, source_label

    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        response.raise_for_status()
        html = response.text
    except requests.exceptions.Timeout:
        print(f"    [!] Timeout : {url}")
        return "", url
    except requests.exceptions.ConnectionError:
        print(f"    [!] Connection error : {url}")
        return "", url
    except requests.exceptions.HTTPError as e:
        print(f"    [!] HTTP {e.response.status_code} : {url}")
        return "", url
    except Exception as e:
        print(f"    [!] Failed : {url} — {e}")
        return "", url

    if is_wikipedia(url):
        clean = parse_wikipedia(html)
        print(f"    [✓] Wikipedia : {source_label}")
    else:
        clean = parse_general(html)
        print(f"    [✓] Fetched   : {source_label}")

    if clean.strip():
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(clean)

    return clean, source_label


def load_urls_from_file(filepath):
    urls = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    urls.append(line)
    except FileNotFoundError:
        print(f"    [i] {filepath} not found — skipping URLs")
    return urls