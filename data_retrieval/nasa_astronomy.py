import requests
from bs4 import BeautifulSoup

def fetch_latest_astronomy_articles():
    """
    Fetches all articles published on the latest day from the NASA Blogs page.
    
    Steps:
      1. Retrieve the NASA Blogs page at https://www.nasa.gov/blogs.
      2. Extract all article elements using a CSS selector for articles with the class 'nasa-blog'.
      3. For each article, extract the published date from the <time> tag by taking the first 10 characters.
      4. Determine the latest date among the articles.
      5. Filter for articles matching that date.
      6. For each filtered article, follow its link and extract:
         - Headline (from an <h1> tag)
         - Full article content (concatenating all <p> tags)
         - Primary image URL (if available)
    
    Returns:
        list: A list of dictionaries, each with keys 'headline', 'content', and 'image_url'.
    """
    blogs_url = "https://www.nasa.gov/blogs"
    response = requests.get(blogs_url)
    if response.status_code != 200:
        raise Exception("Failed to retrieve NASA blogs page")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    # Use a CSS selector for articles with class 'nasa-blog'
    article_elements = soup.select("article.nasa-blog")
    if not article_elements:
        raise Exception("No articles found on NASA blogs page")
    
    # Build a list of (article_element, published_date) tuples.
    articles_info = []
    for article in article_elements:
        time_tag = article.find('time')
        if time_tag and time_tag.has_attr('datetime'):
            # Extract only the date portion (first 10 characters, e.g. "2025-03-06")
            published_date = time_tag['datetime'][:10]
            articles_info.append((article, published_date))
    
    if not articles_info:
        raise Exception("No published dates found for articles")
    
    # Determine the latest published date (dates in ISO format are directly comparable)
    latest_date = max(date for _, date in articles_info)
    
    # Filter articles to those published on the latest date.
    latest_articles = [article for article, date in articles_info if date == latest_date]
    
    results = []
    for article in latest_articles:
        # Extract the article link (assumes the first <a> tag is the link)
        link_tag = article.find('a')
        if not link_tag or not link_tag.has_attr('href'):
            continue
        
        article_url = link_tag['href']
        # Convert relative URLs to absolute.
        if article_url.startswith('/'):
            article_url = "https://www.nasa.gov" + article_url
        
        # Fetch the article's detail page.
        article_response = requests.get(article_url)
        if article_response.status_code != 200:
            continue
        
        article_soup = BeautifulSoup(article_response.text, 'html.parser')
        # Extract the headline (assumed to be in an <h1> tag)
        headline_tag = article_soup.find('h1')
        headline = headline_tag.get_text().strip() if headline_tag else "No headline available"
        
        # Extract the full article content by concatenating all <p> tags.
        paragraphs = article_soup.find_all('p')
        content = "\n".join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
        
        # Extract the first available image URL (if any).
        image_tag = article_soup.find('img')
        image_url = image_tag['src'] if image_tag and image_tag.has_attr('src') else None
        
        results.append({
            'headline': headline,
            'content': content,
            'image_url': image_url
        })
    
    return results