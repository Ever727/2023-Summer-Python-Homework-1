import random
import requests
import re
import csv
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


def solve_info():
    
    num = 1
    with open('url.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for url in lines:
        try:
            url = url.strip()
            proxy = select_proxy()
            headers = {'User-Agent': ua().random}
            response = requests.get(url, headers=headers,
                                    proxies=proxy, verify=True)
            response.encoding = 'UTF-8'
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            if re.search('csj', url):
                pass
            else:
                title = soup.find('h1', class_='main-title').text
                date = soup.find('span', class_='date').text
                editor = ''
                if soup.find('a', class_='source ent-source'):
                    source = soup.find('a', class_='source ent-source').text
                elif soup.find('span', class_='source ent-source'):
                    source = soup.find('span', class_='source ent-source').text
                elif soup.find('span', class_='source'):
                    source = soup.find('span', class_='source').text

                paragraphs = []
                artibody = soup.find('div', class_='article',
                                    attrs={'id': 'artibody'})
                paragraph_pattern = re.compile(r'<p[^>]*>(.*?)</p>')
                pmatches = paragraph_pattern.findall(str(artibody))
                for match in pmatches:
                    if re.search('</a>', match):
                        pass
                    elif re.search('责任编辑：', match):
                        editor = match.replace('责任编辑：', '').strip()
                    else:
                        match = re.sub(r'<\/?strong>', '', match)
                        match = re.sub(r'<\/?font[^>]*>', '', match)
                        match = re.sub(r'<\/?span[^>]*>', '', match)
                        match = match.replace('\u3000', '  ')
                        match = match.replace('\xa0', '')
                        paragraphs.append(match)

                imgbody = soup.find_all('div', class_='img_wrapper')
                img = []
                for div in imgbody:
                    img_tag = div.find('img')
                    img_src = img_tag['src']
                    img.append(img_src)

                keywords_tag = soup.find('div', class_='keywords', attrs={
                                        'data-sudaclick': 'content_keywords_p'})
                if keywords_tag:
                    pattern = re.compile(
                        r'<a href="[^"]+" target="_blank">([^<]+)</a>')
                    matches = pattern.findall(str(keywords_tag))
                    keywords = matches
                else:
                    keywords = []

                with open(f'new_info\{num}.txt', 'w', encoding='utf-8') as f:
                    f.write(url + '\n')
                    f.write(title + '\n')
                    f.write(date + '\n')
                    f.write(source + '\n')
                    f.write(editor + '\n')
                    f.write(' '.join(keywords) + '\n')
                    f.write('\n'.join(paragraphs) + '\n\n')
                    f.write('\n'.join(img) + '\n')
                    num += 1
        except:
            pass

solve_info()
