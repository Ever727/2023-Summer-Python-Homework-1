from django.db import models
from django.utils import timezone

# Create your models here.
class News(models.Model):
    class Meta:
        app_label = 'news'
    url = models.URLField()
    title = models.CharField(max_length=100)
    date = models.DateTimeField()
    source = models.CharField(max_length=100)
    editor = models.CharField(max_length=100)
    keywords = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    imgurl = models.TextField(blank=True)
    views = models.IntegerField(default=0)  # 阅读量
    likes = models.IntegerField(default=0)  # 点赞数
    favorites = models.IntegerField(default=0)  # 收藏数
    comments = models.IntegerField(default=0)  # 评论数
    local_img = models.TextField(blank=True)

class Comment(models.Model):
    class Meta:
        app_label = 'news'
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    user = models.CharField(max_length=10, default='')
    content = models.TextField(max_length=1000)  # 评论内容
    date = models.DateTimeField(auto_now_add=True)