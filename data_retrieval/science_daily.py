import requests
from bs4 import BeautifulSoup
import datetime

def fetch_latest_engineering_articles():
    """
    Fetch the single most recent article from ScienceDaily's Engineering page,
    then parse the full article text and primary image if any.
    
    Returns a dict with:
      {
        'headline': str,
        'date': 'YYYY-MM-DD',
        'link': str,
        'content': str,
        'image_url': str or None
      }
    or None if none found.
    """
    url = "https://www.sciencedaily.com/news/matter_energy/engineering/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise Exception(f"Failed to retrieve page: {resp.status_code} {resp.reason}")
    
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # -- Step 1: Grab all "blocks" that appear to have .latest-head and .latest-summary --
    head_blocks = soup.find_all("div", class_="latest-head")
    if not head_blocks:
        return None
    
    articles = []
    for block in head_blocks:
        link_tag = block.find("a")
        if not link_tag:
            continue
        
        # Headline
        headline = link_tag.get_text(strip=True)
        
        # Build the absolute link
        rel_link = link_tag.get("href", "").strip()
        if rel_link.startswith("/"):
            full_link = "https://www.sciencedaily.com" + rel_link
        else:
            full_link = rel_link
        
        # The date is usually in the sibling div .latest-summary > .story-date
        summary_div = block.find_next_sibling("div", class_="latest-summary")
        if not summary_div:
            continue
        
        date_span = summary_div.find("span", class_="story-date")
        if not date_span:
            continue
        
        raw_date = date_span.get_text(strip=True)  # e.g. "Mar. 6, 2025 —"
        raw_date = raw_date.split("—")[0].strip()   # => "Mar. 6, 2025"
        
        try:
            dt = datetime.datetime.strptime(raw_date, "%b. %d, %Y")
            iso_date = dt.strftime("%Y-%m-%d")
        except ValueError:
            iso_date = None
        
        articles.append({
            "headline": headline,
            "link": full_link,
            "date": iso_date,  # rename iso_date -> date for clarity
        })
    
    if not articles:
        return None
    
    # -- Step 2: Identify the single newest article by date. --
    valid = [a for a in articles if a["date"] is not None]
    if not valid:
        return None
    
    max_date = max(a["date"] for a in valid)
    # If there are multiple same-day articles, pick the first in the list
    newest = next(a for a in valid if a["date"] == max_date)
    
    # -- Step 3: Fetch the detail page of that newest article. --
    detail_resp = requests.get(newest["link"], headers=headers)
    if detail_resp.status_code != 200:
        # If we can't fetch the detail page, at least return the summary info
        newest["content"] = ""
        newest["image_url"] = None
        return newest
    
    detail_soup = BeautifulSoup(detail_resp.text, "html.parser")
    
    # Grab the #story_text section, typically containing paragraphs
    story_div = detail_soup.find("div", {"id": "story_text"})
    if story_div:
        paragraphs = story_div.find_all("p")
        content = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
    else:
        content = ""
    
    # Attempt to find an image
    image_tag = detail_soup.select_one("#story_text figure.image img")
    image_url = image_tag["src"] if (image_tag and image_tag.has_attr("src")) else None
    
    # The final, updated headline from the detail page if available
    detail_headline_tag = detail_soup.select_one("#story_text h1")
    if detail_headline_tag:
        newest["headline"] = detail_headline_tag.get_text(strip=True)
    
    newest["content"] = content
    newest["image_url"] = image_url
    
    return newest
