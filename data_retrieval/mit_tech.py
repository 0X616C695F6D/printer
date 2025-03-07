import requests
from bs4 import BeautifulSoup

def fetch_latest_tech_article():
    """
    Scrapes the latest technology article from MIT Technology Review.
    Extracts the headline and article content.
    
    Returns:
        dict: A dictionary with keys 'headline' and 'content'.
    """
    url = "https://www.technologyreview.com/"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to retrieve MIT Technology Review page")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    article = soup.find('article')
    if not article:
        raise Exception("No article found on MIT Technology Review page")
    
    # Extract headline from h2, h1, or h3 tag
    headline_tag = article.find('h2') or article.find('h1') or article.find('h3')
    headline = headline_tag.get_text().strip() if headline_tag else "No headline available"
    
    # Extract content from the first paragraph tag
    content_tag = article.find('p')
    content = content_tag.get_text().strip() if content_tag else "No content available"
    
    return {
        'headline': headline,
        'content': content
    }

