import jieba
import os
import jieba.analyse
import pickle
from collections import Counter
import json
from collections import defaultdict

# 设置 Django 配置
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pro.settings")

# 导入其他必要的模块
django.setup()
from news.models import News

# 定义一个用于保存倒排索引的字典
inverted_index = defaultdict(list)

# 获取所有新闻对象，并遍历每个新闻对象
for news in News.objects.all():
    # 提取新闻对象的关键词
    keywords = jieba.lcut(news.content)
    # 遍历每个关键词，保存关键词和新闻id之间的对应关系
    for keyword in keywords:
        if keyword.strip() and news.id not in inverted_index[keyword]:
            inverted_index[keyword].append(news.id)

# 将倒排索引保存为json文件
index_dict = {}
for key, value in inverted_index.items():
    index_dict[key] = list(value)

with open('inverted_index.json', 'w', encoding='utf-8') as f:
    json.dump(index_dict, f, ensure_ascii=False)
