import requests
from bs4 import BeautifulSoup

def fetch_latest_stock_article():
    """
    Retrieve the latest stock article from Yahoo Finance by scraping the homepage.
    Extracts the headline, content, and primary image URL from the first <article> found.
    
    Returns:
        dict: A dictionary with keys 'headline', 'content', and 'image_url'.
    """
    url = "https://finance.yahoo.com/"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception("Failed to retrieve Yahoo Finance page")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    article = soup.find('article')
    
    if not article:
        raise Exception("No article found on the page")
    
    # Attempt to find the headline, content, and image URL within the article
    headline_tag = article.find('h3')
    content_tag = article.find('p')
    image_tag = article.find('img')
    
    headline = headline_tag.get_text().strip() if headline_tag else "No headline available"
    content = content_tag.get_text().strip() if content_tag else "No content available"
    image_url = image_tag['src'] if image_tag and image_tag.has_attr('src') else None
    
    return {
        'headline': headline,
        'content': content,
        'image_url': image_url
    }

