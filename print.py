#!/usr/bin/env python3

"""_summary_
author:      ash
date:        2024-05-10 11:33AM
description: read information from API endpoints and format to a printable page
"""

import requests
from datetime import datetime


OUTPUT_PATH  = '/home/ash/.f/day_report.txt'
WSB_BASE_URL = "https://tradestie.com/api/v1/apps/reddit?date="

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

    with open(OUTPUT_PATH, 'w') as file:
        file.write(stocks + '\n')
        file.write(reddit)