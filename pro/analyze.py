import jieba
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from collections import Counter
import os
import django
import numpy as np

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pro.settings")
django.setup()
from news.models import News

# 获取新闻对象列表
news = News.objects.all()

# 获取新闻内容列表
news_content = [n.content for n in news]

# 使用jieba进行分词
segmented_news_content = []
for content in tqdm(news_content, desc="Segmenting"):
    segmented_words = jieba.lcut(content)
    segmented_news_content.append(segmented_words)

# 过滤分词结果，保留长度大于1的词语
filtered_segmented_news_content = []
for segmented_words_list in tqdm(segmented_news_content, desc="Filtering"):
    filtered_segmented_words = []
    for word in segmented_words_list:
        if len(word) > 1:
            filtered_segmented_words.append(word)
    filtered_segmented_news_content.append(' '.join(filtered_segmented_words))

# 使用TfidfVectorizer获取tf-idf特征
vectorizer = TfidfVectorizer()
tfidf_features = vectorizer.fit_transform(filtered_segmented_news_content)

# 使用K-means对数据进行聚类
kmeans = KMeans(n_clusters=10)  # 将数据聚成10个类别
clusters = kmeans.fit_predict(tfidf_features)

# 使用t-SNE将高维特征降维至三维
tsne = TSNE(n_components=3)
X_embedded = tsne.fit_transform(tfidf_features.toarray())

# 将聚类结果和t-SNE降维后的特征矩阵合并
merged_features = np.column_stack((X_embedded, clusters))

# 统计每个类别的数量
cluster_counts = Counter(clusters)

# 设置颜色列表，确保有足够多的不同颜色
colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'purple', 'orange', 'gray', 'brown', 'olive', 'pink', 'teal']

# 绘制三维散点图，并根据聚类结果进行着色
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i in range(len(clusters)):
    ax.scatter(merged_features[i, 0], merged_features[i, 1], merged_features[i, 2], c=colors[clusters[i]])

max_count = max(cluster_counts.values())
bbox_props = dict(boxstyle="round", fc="w", ec="gray", lw=2)  # bbox的样式参数
text_x = 75  # 注释框的x轴位置
text_y = 0  # 注释框的y轴位置
text_z = 0  # 注释框的z轴位置
text_spacing = 60  # 调整注释框之间的间距
for cluster, count in cluster_counts.items():
    text_z += text_spacing
    ax.text(text_x, text_y, text_z, f'Cluster {cluster}: {count}', bbox=bbox_props, color=colors[cluster])

plt.show()
