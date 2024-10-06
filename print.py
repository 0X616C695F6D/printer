#!/usr/bin/env python3

"""_summary_
author:      ash
date:        2024-05-10 11:33AM
description: read information from API endpoints and format to a printable page
"""

import requests
from datetime import datetime


WSB_BASE_URL = "https://tradestie.com/api/v1/apps/reddit?date="

def fetch_wsb_stocks():
    current_date = datetime.now().strftime('%Y-%m-%d')
    wsb_url = f"{WSB_BASE_URL}{current_date}"
    print(wsb_url)

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