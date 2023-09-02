import random
from datetime import datetime

import os
from django.conf import settings

# 设置 Django 配置
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pro.settings")

# 导入其他必要的模块
import django

#settings.configure()
django.setup()

from news.models import News

for num in range(1, 7226):
    with open(f'D:\\Program\\Python\\new_info\\{num}.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    views = random.randint(0, 100000)
    news = News(
        url=lines[0].strip(),
        title=lines[1].strip(),
        date=datetime.strptime(lines[2].strip(), '%Y年%m月%d日 %H:%M'),
        source=lines[3].strip(),
        editor=lines[4].strip(),
        keywords=lines[5].strip(),
        content='\n'.join([line for line in lines[6:]
                          if not line.strip().startswith(('//', '<', 'http', 'https'))]),
        imgurl='\n'.join([line.strip() for line in lines[7:]
                         if line.strip().startswith(('//', 'http', 'https'))]),
        views=views,
        likes=random.randint(0, views),
        favorites=random.randint(0, views),
       comments=0
    )
    news.save()
    #news.full_clean()
