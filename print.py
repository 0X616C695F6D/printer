#!/usr/bin/env python3

"""_summary_
author:      ash
date:        2024-05-10 11:33AM
description: read information from API endpoints and format to a printable page
"""

import time
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta


OUTPUT_PATH  = '/home/ash/.f/day_report.txt'
WSB_BASE_URL = "https://tradestie.com/api/v1/apps/reddit?date="
ARXIV_URL    = "http://export.arxiv.org/api/query"

# Pull JSON from tradestie and output only top 5 bullish and bearish stocks
# This API displays the sentiment of stocks in WSB for the current date
def fetch_wsb_stocks():
    current_date = datetime.now().strftime('%Y-%m-%d')
    wsb_url = f"{WSB_BASE_URL}{current_date}"
    #print(wsb_url)

    response = requests.get(wsb_url)
    stock_data = response.json()

    bulls = [stock for stock in stock_data if stock['sentiment'] == 'Bullish'][:5]
    bears = [stock for stock in stock_data if stock['sentiment'] == 'Bearish'][:5]
    
    return bulls, bears

def format_stock_entry(stock):
    return f"{stock['ticker']}: {stock['sentiment_score']:.2f}"

def format_stocks(bulls, bears, width=78):
    result = ""
    col_width = width // 2
    max_len = max(len(bulls), len(bears))

    for i in range(max_len):
        bulls_txt = format_stock_entry(bulls[i]) if i < len(bulls) else ''
        bears_txt = format_stock_entry(bears[i]) if i < len(bears) else ''

        result += bulls_txt.ljust(col_width) + bears_txt.ljust(col_width) + '\n'
    
    return result


# Pull subreddit posts and print the top headlines
# Use this as an additional community-based news source, not for anything important
# I.e. reddit is a bunch of bs~
def fetch_sub_reddits(subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/top/.json"
    headers = {'User-agent': 'Mozilla/5.0'}
    
    response = requests.get(url, headers=headers, params={'limit': 5})
    data = response.json()

    top_posts = [post['data']['title'] for post in data['data']['children']]

    return top_posts

def format_reddit(subreddit):
    top_posts = fetch_sub_reddits(subreddit)

    reddit_report = f"--- r/{subreddit} ---\n\n"
    for i, post in enumerate(top_posts, 1):
        reddit_report += f"{i}. {post}\n"
    return reddit_report


# Arxiv papers. The output is Atom format.
# Filter gives only 3 papers of recent publishing dates.
# Could use more work to pick good papers, but okay for now.
def fetch_arxiv(category, date):
    formatted_date = date.strftime('%Y-%m-%d')

    params = {
        'search_query': f'cat:{category}',
        'start':'0',
        'max_results':'3',
        'sortBy':'submittedDate',
        'sortOrder':'descending'
    }

    response = requests.get(ARXIV_URL, params=params)
    root = ET.fromstring(response.content)

    papers = []
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
        authors = [author.find('{http://www.w3.org/2005/Atom}name').text.strip() for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
        published_date = entry.find('{http://www.w3.org/2005/Atom}published').text.strip()
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()

        papers.append({
            'title': title,
            'authors': authors,
            'published_date':published_date,
            'summary': summary,
        })
    return papers


if __name__ == "__main__":
    stocks = f'--- Stocks ---\n\n'
    bulls, bears  = fetch_wsb_stocks()
    stocks += format_stocks(bulls, bears)
    #print(stocks)

    reddit = ''
    subreddits = ['wallstreetbets', 'worldnews', 'Futurology', 'technews']
    for subs in subreddits:
        reddit += format_reddit(subs) + '\n'
    #print(reddit)

    # arxiv taxonomies can be found here: https://arxiv.org/category_taxonomy
    # API requests are rate limited; for safety use 10 second timeouts
    yesterday = datetime.now() - timedelta(days=1)
    arxiv  = fetch_arxiv('cs.AI', yesterday.date()) # Artifical intelligence
    time.sleep(10)
    arxiv += fetch_arxiv('cs.CR', yesterday.date()) # Cryptography and security
    time.sleep(10)
    arxiv += fetch_arxiv('eess.SP', yesterday.date()) # Signal processing

    arxiv_out = "--- Arxiv ---\n\n"
    for i, paper in enumerate(arxiv):
        arxiv_out += f"Title: {paper['title']}\n"
        arxiv_out += f"Authors: {paper['authors']}\n"
        arxiv_out += f"Published date: {paper['published_date']}\n\n"
        arxiv_out += f"{paper['summary']}\n\n"

    print(arxiv_out)

    with open(OUTPUT_PATH, 'w') as file:
        file.write(stocks + '\n')
        file.write(reddit)
        file.write(arxiv_out)
