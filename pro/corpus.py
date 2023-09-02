import jieba
import os
import jieba.analyse
import pickle
from collections import Counter
# 设置 Django 配置
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pro.settings")

# 导入其他必要的模块


#settings.configure()
django.setup()
from news.models import News

# 获取所有新闻内容及其对应的 ID
news_data = [(news.id, news.content) for news in News.objects.all()]

# 将所有新闻内容合并为一个字符串
corpus = ' '.join(news_content for _, news_content in news_data)

# 提取关键词及其对应的 IDF 值
keywords = jieba.analyse.extract_tags(corpus, topK=None, withWeight=True)
idf_dict = {word: weight for word, weight in keywords}

# 构建 TF-IDF 字典库
tfidf_dict = {}
for news_id, news_content in news_data:
    # 统计每个关键词在当前新闻中出现的次数
    word_counts = Counter(jieba.cut(news_content, HMM=False))
    total_words = sum(word_counts.values())
    
    # 计算每个关键词的 TF 值，并乘以对应的 IDF 值得到 TF-IDF 值
    tfidf_values = {word: tf * idf_dict.get(word, 0) for word, tf in word_counts.items()}
    
    # 将当前新闻的 TF-IDF 值存入字典库中
    tfidf_dict[news_id] = tfidf_values

# 保存 TF-IDF 字典库为 pickle 文件
with open('tfidf_dict.pickle', 'wb') as f:
    pickle.dump(tfidf_dict, f)