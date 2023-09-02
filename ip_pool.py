import random
import requests
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent as ua


def find_ip_pool():
    proxies_url = "http://www.66ip.cn/"
    headers = {'User-Agent': ua().random}
    total_pages = 200

    for page in range(102, total_pages + 1):
        try:
            r = requests.get(proxies_url + str(page) +
                             '.html', headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            ip_table = soup.find("table", attrs={"bordercolor": "#6699ff"})
            ip_rows = ip_table.find_all("tr")[1:]

            for row in ip_rows:
                ip_port = re.findall(
                    r'<td>(\d+\.\d+\.\d+\.\d+)</td><td>(\d+)</td>', str(row))
                for item in ip_port:
                    ip, port = item
                    proxy = {
                        "http": "http://{}:{}".format(ip, port),
                        "https": "https://{}:{}".format(ip, port)
                    }
                    try:
                        response = requests.get(
                            "http://httpbin.org/ip", proxies=proxy, timeout=5)
                        if response.status_code == 200:
                            with open('ip_pool.txt', 'a', encoding='utf-8') as f:
                                f.write(ip + ' ' + port + '\n')
                    except:
                        pass

        except requests.RequestException as e:
            print(f"Find ip pool error: {e}")


find_ip_pool()
