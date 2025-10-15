from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re
import datetime
import os

# 直接获取实时金价
gold_price = None
buy_weight = 0  # 默认值

# 设置无头浏览器
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
except Exception as e:
    # 如果自动安装失败，尝试手动指定 chromedriver 路径
    chromedriver_path = "/usr/bin/chromedriver"  # 容器中的默认路径
    if os.path.exists(chromedriver_path):
        driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)
    else:
        raise Exception(f"无法找到 chromedriver: {e}")

# 目标页面
url = 'https://m.jr.jd.com/finance-gold/msjgold/homepage?from=fhc&ip=66.249.71.78&orderSource=6&ptag=16337378.0.1'

try:
    driver.get(url)
    time.sleep(3)  # 等待JS渲染

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 提取实时金价
    all_titles = soup.find_all('span', class_='gold-price-persent-title')
    gold_price = None
    for title in all_titles:
        if '实时金价' in title.get_text():
            match = re.search(r'(\d+\.\d+)', title.get_text())
            if match:
                gold_price = float(match.group(1))
                break

    if gold_price:
        # 当前时间（时间戳格式）
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp = int(time.time())
        print(f"{now} 实时金价: {gold_price} 元/克")
        # 保存金价和时间到文件
        # with open("gold_price.txt", "a") as file:
        #     file.write(f"{timestamp},{gold_price}\n")
    else:
        print("未找到实时金价")
except Exception as e:
    print(f"获取金价时出错: {e}")
finally:
    driver.quit()

def get_current_price():
    """
    获取实时金价
    :return: 实时金价（浮点数）
    """
    global gold_price
    return gold_price