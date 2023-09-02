from django.db import models

# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=30)
    blog_content = models.CharField(max_length=2000)


class Comment(models.Model):
    # 将Blog作为外键，Blog删除时级联删除所有的Comment
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.CharField(max_length=10)
    comment_content = models.CharField(max_length=1000)
