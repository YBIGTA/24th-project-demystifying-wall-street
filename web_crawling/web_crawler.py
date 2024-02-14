from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import numpy as np
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
# import selenium
from selenium import webdriver
import undetected_chromedriver as uc
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
import requests
from zenrows import ZenRowsClient
from bs4 import BeautifulSoup

client = ZenRowsClient("04b5768a40a0533b80959905b6034b472ad61aa4")
url = "https://www.bloomberg.com/news/articles/2024-02-11/five-key-charts-to-watch-in-global-commodity-markets-this-week?srnd=industries-v2"
params = {"js_render":"true","block_resources":"media,xhr,eventsource,image"}

response = client.get(url, params=params)
soup = BeautifulSoup(response.text, "html.parser")

blb_news = pd.DataFrame(columns=['URL','h1','text'])

title = soup.find("h1").text
p_tags = soup.find_all('p', attrs={'class': ['Paragraph_text-SqIsdNjh0t0-', 'Paragraph_text-SqIsdNjh0t0- paywall']})

text_content = ""
for p in p_tags:
    text_content += p.text + " "
text_content = text_content.strip()

blb_news = blb_news._append(
    {"URL": url,
     "h1": title,
     "text": text_content},
    ignore_index=True
)

blb_news
blb_news['text'][0]

def get_yf_news(url):

    '''driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(2)'''

    options = webdriver.ChromeOptions()
    options.add_argument('proxy-server=172.67.134.0:80')
    options.add_argument("--disable-cache")
    browser = uc.Chrome(
        options = options
    )
    browser.get(url)
    browser.implicitly_wait(2)

    try:
        for web_page in range(2):
            interval = 1 
            prev_height = browser.execute_script("return document.body.scrollHeight")

            while True:
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(interval)
                curr_height = browser.execute_script("return document.body.scrollHeight")
                if curr_height == prev_height:
                    break
                prev_height = curr_height

            #try:
                #browser.execute_script("arguments[0].click();", WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CLASS_NAME,"collapse-button"))))
            #except Exception as e:
                #print(f"Error: {str(e)}")

        news_url = []
        
        hrefs = [element.get_attribute("href") for element in browser.find_elements(By.XPATH, "//*[@href]")]

        for href in hrefs:
            if href.endswith('.html'):
                news_url.append(href)

        news = pd.DataFrame(columns=['url', 'h1', 'text'])

        for url in news_url[:1]:
            if url.endswith('.html'):
                news_url.append(url)

            h1 = browser.find_element(By.TAG_NAME, 'h1')
            h1 = h1.text 

            p_tags = browser.find_elements(By.TAG_NAME, 'p')

            text_content = ""
            for p in p_tags:
                text_content += p.text + " "
            text_content = text_content.strip()

            news = news._append({'url': url, 'h1': ''.join(h1), 'text': text_content}, ignore_index=True)
            return news
        
    finally:
        browser.delete_all_cookies()
        browser.quit()

# Undetected Chromedriver took 35.5 seconds to scrape the news
# Incognito Chrome took 44.2 seconds to complete the same task

yf_news = get_yf_news("https://finance.yahoo.com/news/analysts-made-financial-statement-dws-060237470.html")
yf_news['text'][0]


def get_wsj_news(url):

    options = webdriver.ChromeOptions()
    # https://hidemy.io/en/proxy-list/ 에서 proxy server 가져오시면 되는데 스피드가 가장 좋은 서버를 선택하면 크롤링도 빨라지더라구요..!
    options.add_argument('proxy-server=172.67.134.0:80')
    options.add_argument("--disable-cache")
    browser = uc.Chrome(
        options = options
    )
    browser.get(url)
    browser.implicitly_wait(2)

    try:
        for web_page in range(2):
            interval = 1
            prev_height = browser.execute_script("return document.body.scrollHeight")

            while True:
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(interval)
                curr_height = browser.execute_script("return document.body.scrollHeight")
                if curr_height == prev_height:
                    break
                prev_height = curr_height


        news_url = []
        
        hrefs = [element.get_attribute("href") for element in browser.find_elements(By.XPATH, "//*[@href]")]

        for href in hrefs:
            news_url.append(href)

        news = pd.DataFrame(columns=['url', 'h1', 'text'])

        for url in news_url[:1]:
            news_url.append(url)

            h1 = browser.find_element(By.TAG_NAME, 'h1')
            h1 = h1.text 

            p_tags = browser.find_elements(By.CLASS_NAME, 'e1e4oisd0')

            text_content = ""
            for p in p_tags:
                text_content += p.text + " "
            text_content = text_content.strip()

            news = news._append({'url': url, 'h1': ''.join(h1), 'text': text_content}, ignore_index=True)
            return news
        
    finally:
        browser.delete_all_cookies()
        browser.quit()
wsj_news = get_wsj_news('https://www.wsj.com/finance/investing/your-mutual-fund-stinks-can-this-wall-street-invention-change-that-73e86075?mod=finance_lead_pos5')
wsj_news
wsj_news['text'][0]



from apify_client import ApifyClient

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_V1gbX5j6ahA4X59BYyUPrwNieXVgy31ttGAy")

# Prepare the Actor input with the extendOutputFunction field containing JavaScript code for web scraping
run_input = {
    "articleUrls": [{"url": "https://www.cnbc.com/2024/02/11/top-wall-street-analysts-pick-these-3-dividend-stocks-for-the-long-haul.html"}],
    "pageWaitMs": 100,
    "scrollToBottomMaxSecs": 2,
    "proxyConfiguration": {"useApifyProxy": True},
    "useGoogleBotHeaders": True
}

# Run the Actor and wait for it to finish
run = client.actor("lukaskrivka/article-extractor-smart").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
cnbc_news = pd.DataFrame(columns=['URL','h1','text'])
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    cnbc_news = cnbc_news._append(
        {"URL": item['url'],
         "h1": item['title'],
         "text": item['text']},
        ignore_index=True
    )
cnbc_news
# Dropping any '\n' and '\' characters from the text
cnbc_news['text'][0] = cnbc_news['text'][0].replace('\n', ' ')
cnbc_news['text'][0] = cnbc_news['text'][0].encode().decode('unicode_escape')
# cnbc_news['text'][0] = cnbc_news['text'][0].replace("\\'","'")
# cnbc_news['text'][0] = cnbc_news['text'][0].split('\\')
# cnbc_news['text'][0] = ' '.join(cnbc_news['text'][0])
cnbc_news['text'] = cnbc_news['text'].iloc[0]
cnbc_news
cnbc_news['text'].iloc[0]
test = " the company\'s "
new_test = test.replace('\\\'', "'")
print(new_test)

test = " the company\'s "
new_test = test.split('\\')
new_test = ''.join(new_test).strip()
new_test




from apify_client import ApifyClient

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_V1gbX5j6ahA4X59BYyUPrwNieXVgy31ttGAy")

# Prepare the Actor input with the extendOutputFunction field containing JavaScript code for web scraping
run_input = {
    "articleUrls": [{"url": "https://www.forbes.com/sites/karlfreund/2024/02/09/why-nvidia-is-entering-the-30b-market-for-custom-chips/?sh=39ac09bd6d290"}],
    "pageWaitMs": 100,
    "scrollToBottomMaxSecs": 2,
    "proxyConfiguration": {"useApifyProxy": True},
    "useGoogleBotHeaders": True
}

# Run the Actor and wait for it to finish
run = client.actor("lukaskrivka/article-extractor-smart").call(run_input=run_input)

fb_news = pd.DataFrame(columns=['URL','h1','text'])
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    fb_news = fb_news._append(
        {"URL": item['url'],
         "h1": item['title'],
         "text": item['text']},
        ignore_index=True
    )
    
fb_news
fb_news['text'][0] = fb_news['text'][0].replace('\n', ' ')
fb_news['text'] = fb_news['text'].iloc[0]
fb_news['text'][0]

