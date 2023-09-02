import random
import requests
import re
import json
import lxml
from bs4 import BeautifulSoup
from fake_useragent import UserAgent as ua


def select_proxy():
    with open('ip_pool.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        ip = random.choice(lines)
        ip = ip.strip()
        ip, port = ip.split()
        proxy = {
            "http": "https://{}:{}".format(ip, port)
        }
    return proxy


def select_news_url(num):
    with open('news_url.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        url = lines[num]
        url = url.strip()
        return url


def get_url(num, date, time):
    url = f"https://feed.mix.sina.com.cn/api/roll/get?pageid=372&lid=2431&etime={time - 86400}&stime={time}&ctime={time}&date=2023-01-{date}&k=&num=50&page={num}&r=0.11847647285867047&callback=jQuery111207471771617184421_1693199686303&_=1693199686304"
    proxy = select_proxy()
    headers = {'User-Agent': ua().random}
    response = requests.get(url, headers=headers, proxies=proxy, verify=True)
    response.encoding = 'UTF-8'
    html = response.text
    with open('ans.txt', 'w', encoding='utf-8') as f:
        f.write(html + '\n')
    pattern = r'"url":"(https:\\\/\\\/[^"]+\.shtml)"'
    matches = re.findall(pattern, html)
    for match in matches:
        match = match.replace('\\', '')
        with open('url.txt', 'a', encoding='utf-8') as f:
            f.write(match + '\n')
    #soup = BeautifulSoup(html, 'lxml')
    #news_rows = soup.find_all('span', class_='c_tit')
    #for row in news_rows:
    #    news_url = re.search(r'href="(.+?)" ', str(row))
    #    if news_url:
    #        with open('output.txt', 'a', encoding='utf-8') as f:
    #            f.write(str(news_url.group(1)) + '\n')
    #    else:
    #        pass

time = 1675180800
for date in reversed(range(1,29)):
    get_url(1, date, time)
    get_url(2, date, time)
    time -= 86400
