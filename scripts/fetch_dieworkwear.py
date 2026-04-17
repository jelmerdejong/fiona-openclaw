#!/usr/bin/env python3
"""
Fetches Derek Guy's dieworkwear.com articles from 2022-2026 and creates
Obsidian markdown pages for each one.
"""

import os
import re
import json
import time
import html
import urllib.request
import urllib.error
from datetime import datetime
from html.parser import HTMLParser

OUTPUT_DIR = "/home/fiona/.openclaw/workspace/vaults/wardrobe/Style/Research/Derek Guy/Web"

# Articles to skip (Black Friday sales, sale roundups, Cuttings, promotional)
SKIP_SLUGS = {
    "six-more-great-black-friday-sales",
    "seven-great-black-friday-sales-2",
    "cuttings",
    "ten-of-the-best-black-friday-sales",
    "a-dozen-great-black-friday-sales",
    "the-best-of-this-seasons-sales",
    "more-black-friday-sales",
    "black-friday-sales-start",
    "no-man-walks-alone-weekend-sale",
    "no-man-walks-alones-winter-sale",
}

# Also skip by title keywords
SKIP_TITLE_KEYWORDS = [
    "black friday",
    "sale",
    "cuttings",
]

class HTMLToText(HTMLParser):
    """Convert HTML to plain text."""
    def __init__(self):
        super().__init__()
        self.result = []
        self.in_skip = 0
        self.skip_tags = {'script', 'style', 'noscript'}
        
    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in self.skip_tags:
            self.in_skip += 1
        elif tag == 'p':
            self.result.append('\n\n')
        elif tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.result.append('\n\n')
        elif tag == 'li':
            self.result.append('\n- ')
        elif tag == 'br':
            self.result.append('\n')
        elif tag == 'a':
            pass  # We skip link URLs
            
    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in self.skip_tags:
            self.in_skip -= 1
        elif tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.result.append('\n')
            
    def handle_data(self, data):
        if not self.in_skip:
            self.result.append(data)
            
    def get_text(self):
        return ''.join(self.result)


def html_to_text(html_content):
    """Convert HTML to clean plain text."""
    parser = HTMLToText()
    parser.feed(html_content)
    text = parser.get_text()
    # Decode HTML entities
    text = html.unescape(text)
    # Clean up excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()


def sanitize_filename(title, max_len=80):
    """Sanitize title for use as filename."""
    # Replace special chars with nothing or spaces
    title = re.sub(r'[^\w\s\-]', '', title)
    title = re.sub(r'\s+', ' ', title).strip()
    if len(title) > max_len:
        title = title[:max_len].rstrip()
    return title


def infer_tags(title, content):
    """Infer topic tags from content."""
    tags = ["derek-guy", "research"]
    text = (title + " " + content).lower()
    
    tag_keywords = {
        "shirts": ["shirt", "ocbd", "oxford cloth", "button-down", "chambray", "flannel", "western shirt", "camp collar"],
        "denim": ["denim", "jeans", "selvedge", "raw denim"],
        "shoes": ["shoe", "boot", "loafer", "sneaker", "footwear", "oxford", "derby", "bespoke shoe", "shoemaking"],
        "outerwear": ["jacket", "coat", "outerwear", "overcoat", "field jacket", "barbour", "waxed", "parka", "anorak", "raincoat", "chore coat"],
        "knitwear": ["sweater", "knit", "wool", "cashmere", "cardigan", "shetland", "crewneck"],
        "tailoring": ["suit", "blazer", "tailoring", "bespoke", "sport coat", "tailor", "lapel"],
        "shopping": ["sale", "shop", "buy", "store", "brand", "retailer"],
        "brands": ["brand", "label", "collection", "designer"],
        "fit": ["fit", "proportion", "silhouette", "size", "alteration"],
        "fabric": ["fabric", "cloth", "cotton", "linen", "wool", "silk", "material", "textile"],
        "color": ["color", "colour", "palette", "tone", "neutral"],
        "accessories": ["watch", "belt", "bag", "accessory", "tie", "pocket square", "jewelry", "necklace"],
        "seasonal": ["spring", "summer", "fall", "autumn", "winter", "seasonal", "season"],
        "basics": ["basic", "essential", "wardrobe", "staple", "foundation"],
        "layering": ["layer", "layering", "under", "over", "beneath"],
        "trousers": ["trouser", "pant", "chino", "khaki", "corduroy"],
        "history": ["history", "historical", "origin", "century", "era"],
        "taste": ["taste", "style", "aesthetic", "develop"],
    }
    
    for tag, keywords in tag_keywords.items():
        if any(kw in text for kw in keywords):
            tags.append(tag)
    
    return tags


def fetch_url(url, retries=3):
    """Fetch URL with retries."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            if attempt < retries - 1:
                print(f"  Retry {attempt+1} for {url}: {e}")
                time.sleep(2)
            else:
                raise


def get_all_posts():
    """Get all posts from 2022+ using WordPress REST API."""
    url = "https://dieworkwear.com/wp-json/wp/v2/posts?per_page=100&after=2022-01-01T00:00:00&page=1&_fields=id,slug,title,date,link"
    data = json.loads(fetch_url(url))
    return data


def get_post_content(post_id):
    """Get full post content via API."""
    url = f"https://dieworkwear.com/wp-json/wp/v2/posts/{post_id}?_fields=id,title,date,link,content,excerpt"
    data = json.loads(fetch_url(url))
    return data


def create_article_file(post, content_html, existing_filenames=None):
    """Create Obsidian markdown file for article."""
    title = html.unescape(post['title']['rendered'])
    url = post['link']
    date_str = post['date'][:10]  # YYYY-MM-DD
    year = date_str[:4]
    slug = post['slug']
    
    # Convert HTML to text
    full_text = html_to_text(content_html)
    
    # Infer tags
    tags = infer_tags(title, full_text[:3000])
    
    # Generate summary (first meaningful paragraph)
    paragraphs = [p.strip() for p in full_text.split('\n\n') if len(p.strip()) > 100]
    summary_text = ' '.join(paragraphs[:2])[:600] + "..." if len(paragraphs) >= 2 else (paragraphs[0][:600] + "..." if paragraphs else "")
    
    # Generate key takeaways (extract key sentences/lists)
    takeaways = extract_takeaways(full_text, title)
    
    # Relevance line
    relevance = infer_relevance(title, tags)
    
    # Build tags YAML
    tags_yaml = "[" + ", ".join(tags) + "]"
    
    # Build markdown
    content = f"""---
source: "dieworkwear.com"
author: "Derek Guy"
url: "{url}"
date: "{date_str}"
tags: {tags_yaml}
---

# {title}

## Summary
{summary_text}

## Key Takeaways
{takeaways}

## Relevance
{relevance}

## Full Text
{full_text}
"""
    
    # Sanitize filename - add year suffix if duplicate
    base_name = sanitize_filename(title)
    filename = base_name + ".md"
    if existing_filenames and filename.lower() in [f.lower() for f in existing_filenames]:
        filename = base_name + f" {year}.md"
    
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filename


def extract_takeaways(text, title):
    """Extract key takeaways from article text."""
    # Look for existing bullet points in text
    lines = text.split('\n')
    bullets = [l.strip() for l in lines if l.strip().startswith('- ') and len(l.strip()) > 20]
    
    if bullets:
        return '\n'.join(bullets[:6])
    
    # Extract key sentences from first few paragraphs
    paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 80]
    takeaways = []
    for para in paragraphs[1:5]:
        # Get first sentence
        sentences = re.split(r'(?<=[.!?])\s+', para)
        if sentences and len(sentences[0]) > 40:
            takeaways.append(f"- {sentences[0][:200]}")
    
    if takeaways:
        return '\n'.join(takeaways[:5])
    
    return "- See full text for detailed advice"


def infer_relevance(title, tags):
    """Generate relevance line for heritage casual wardrobe."""
    title_lower = title.lower()
    
    if "shirt" in title_lower:
        return "Core reading for building a versatile shirt wardrobe including OCBDs, chambrays, flannels, and Western shirts."
    elif "taste" in title_lower:
        return "Essential philosophy for building a refined, considered wardrobe rooted in personal aesthetic rather than trends."
    elif "tailoring" in title_lower or "suit" in title_lower:
        return "Relevant for understanding how to integrate tailored pieces with heritage casual staples."
    elif "shoe" in title_lower or "bespoke shoe" in title_lower.replace("shoemaking", "shoe"):
        return "Valuable for understanding quality footwear that pairs with heritage casual wardrobe — boots, loafers, derbies."
    elif "spring" in title_lower or "fall" in title_lower or "excited to wear" in title_lower:
        return "Seasonal inspiration for heritage casual dressing featuring field jackets, OCBDs, chinos, quality basics, and selvedge denim."
    elif "brand" in title_lower or "new brand" in title_lower:
        return "Introduces quality brands producing heritage-adjacent and workwear-influenced clothing worth tracking."
    elif "bookcore" in title_lower:
        return "Directly relevant — heritage casual aesthetic overlaps with the bookish, relaxed, quality-focused wardrobe described."
    elif "babenzien" in title_lower or "j. crew" in title_lower:
        return "Relevant for understanding how accessible labels approach classic American heritage casualwear."
    elif "akamine" in title_lower:
        return "Rare insight from a Japanese menswear legend on classic dressing principles that apply directly to heritage casual style."
    elif "space cowboy" in title_lower or "american" in title_lower:
        return "Explores American workwear and outdoor heritage aesthetics relevant to field jacket and chino wardrobe building."
    elif "polo coat" in title_lower or "outerwear" in tags:
        return "Covers outerwear choices that complement a heritage casual wardrobe — coats, field jackets, and layering pieces."
    else:
        return "Relevant for building a refined heritage casual wardrobe with quality basics and thoughtful style choices."


def should_skip(post):
    """Determine if post should be skipped."""
    slug = post['slug']
    title = post['title']['rendered'].lower()
    
    if slug in SKIP_SLUGS:
        return True, f"slug in skip list"
    
    for keyword in SKIP_TITLE_KEYWORDS:
        if keyword in title and ("sale" in slug or "black-friday" in slug or "cuttings" in slug):
            return True, f"title/slug match skip keyword: {keyword}"
    
    return False, ""


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("Fetching post list from WordPress API...")
    posts = get_all_posts()
    print(f"Found {len(posts)} posts from 2022+")
    
    saved = []
    skipped = []
    errors = []
    saved_filenames = []
    
    for i, post in enumerate(posts):
        title = html.unescape(post['title']['rendered'])
        slug = post['slug']
        date = post['date'][:10]
        
        # Check skip
        skip, reason = should_skip(post)
        if skip:
            print(f"  SKIP [{date}] {title} ({reason})")
            skipped.append(title)
            continue
        
        print(f"  [{i+1}/{len(posts)}] Fetching: {title} ({date})")
        
        try:
            # Get full content
            full_post = get_post_content(post['id'])
            content_html = full_post.get('content', {}).get('rendered', '')
            
            if not content_html:
                print(f"    WARNING: No content for {title}")
                errors.append(f"No content: {title}")
                continue
            
            filename = create_article_file(post, content_html, existing_filenames=saved_filenames)
            saved_filenames.append(filename)
            saved.append({"title": title, "date": date, "file": filename})
            print(f"    Saved: {filename}")
            
            # Rate limit
            time.sleep(0.5)
            
        except Exception as e:
            print(f"    ERROR: {e}")
            errors.append(f"{title}: {e}")
    
    print(f"\n{'='*60}")
    print(f"COMPLETE: {len(saved)} articles saved, {len(skipped)} skipped, {len(errors)} errors")
    
    if saved:
        print(f"\nSaved articles:")
        for s in saved:
            print(f"  [{s['date']}] {s['title']}")
    
    if errors:
        print(f"\nErrors:")
        for e in errors:
            print(f"  {e}")
    
    # Write a summary JSON
    with open(os.path.join(OUTPUT_DIR, "_index.json"), 'w') as f:
        json.dump({"saved": saved, "skipped": skipped, "errors": errors}, f, indent=2)
    
    return saved


if __name__ == "__main__":
    main()
