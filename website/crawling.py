from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np
import time
import re
import selenium
from selenium import webdriver
import undetected_chromedriver as uc
import random
import requests
from bs4 import BeautifulSoup
from apify_client import ApifyClient
from zenrows import ZenRowsClient



def url_parser(url):

    user_url = url.split('/')
    keyword = user_url[2].split('.')

    if 'bloomberg' or 'reuters' in keyword:
        blb_news = zenrows(url)
        return blb_news
    elif 'yahoo' in keyword:
        yf_news = normal_requests(url)
        return yf_news
    elif 'cnbc' in keyword or 'forbes' or 'theguardian' or 'sky' in keyword:
        c_f_news = apify_news(url)
        return c_f_news
    else:
        try:
            return normal_requests(url)
        except Exception as e:
            return f"Source cannot be supported due to error: {str(e)}"


def zenrows(url):
    client = ZenRowsClient("04b5768a40a0533b80959905b6034b472ad61aa4")
    user_url = url 
    params = {"js_render":"true","block_resources":"media,xhr,eventsource,image"}

    response = client.get(user_url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")

    news = {
        "title": soup.find("h1").text,
        "text": " ".join([p.text for p in soup.find_all('p')]).replace('\n', ' ').replace('\\', '')
    }

    return news


def apify_news(url):

    client = ApifyClient("apify_api_V1gbX5j6ahA4X59BYyUPrwNieXVgy31ttGAy")
    user_url = url
    run_input = {
        "articleUrls": [{"url": user_url}],
        "pageWaitMs": 100,
        "scrollToBottomMaxSecs": 2,
        "proxyConfiguration": {"useApifyProxy": True},
        "useGoogleBotHeaders": True
    }

    run = client.actor("lukaskrivka/article-extractor-smart").call(run_input=run_input)
    
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        news = {
            "title": item['title'],
            "text": item['text']
        }

    return news


def normal_requests(url):

    headers = { 
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    session = requests.Session()
    session.headers.update(headers)
    session.cookies.clear()
    response = session.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        news = {
        "title": soup.find("h1").text,
        "text": " ".join([p.text for p in soup.find_all('p')]).replace('\n', ' ').replace('\\', '')
    }
        return news
    else:
        print(f"Error: {response.status_code} and {response.text}")
