from django.shortcuts import render

# Create your views here.
from .models import Blog, Comment
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

def show_blog(request, id): # 这里 request 是 HttpRequest 类型的对象
    blog = Blog.objects.get(id=id) # 数据库查询操作
    template = loader.get_template('blog/index.html')
    context = {
        'blog_id': id,
        'blog_title': blog.title,
        'blog_content': blog.blog_content,
        'comments': blog.comment_set.all() # 通过外键反向查询
    }
    return HttpResponse(template.render(context, request)) # 返回渲染好的html

def comment(request, id): 
    data = request.POST
    # 将新的消息添加到数据库中
    user = data['user']
    comment_content = data['content']
    blog = Blog.objects.get(id=id)
    obj = Comment(blog=blog, user=user, comment_content=comment_content)
    obj.full_clean() #对数据进行验证
    obj.save() #存储在表中
    return HttpResponseRedirect(f'/index/blog/{id}') # 将页面重定向到博客的url