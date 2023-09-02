import os
import random
import requests
from fake_useragent import UserAgent as ua
import hashlib

# 设置 Django 配置
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pro.settings")

# 导入其他必要的模块
django.setup()
from news.models import News

news_list = News.objects.all()

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

for news in news_list:
    if news.imgurl:
        try:
            local_img_paths = []
            imgurls = news.imgurl.split('\n')
            for imgurl in imgurls:
                if not imgurl.startswith('http'):
                    imgurl = 'https:' + imgurl
                proxy = select_proxy()
                headers = {'User-Agent': ua().random}
                response = requests.get(imgurl, headers=headers, proxies=proxy, verify=True)
                image = response.content
                # 获取文件名和后缀
                filename = imgurl.split('/')[-1]
                file_extension = os.path.splitext(filename)[1]  # 获取文件后缀
                # 使用哈希值生成唯一的文件名
                file_hash = hashlib.md5(image).hexdigest()
                filename = file_hash + file_extension
                file_path = os.path.join('D:\Program\Python\pro\static', filename)
                with open(file_path, 'wb') as f:
                    f.write(image)
                #image_path = os.path.abspath(file_path)
                local_img_paths.append(filename)
            local_img_str = '\n'.join(local_img_paths)
            news.local_img = local_img_str
            news.save()
        except:
            pass