from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from news.models import News, Comment
from datetime import datetime
from django.db.models import F, Q
from django.utils import formats
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.db.models.functions import Length
import json
import jieba
import re

# Create your views here.


def show_home(request):
    news = News.objects.order_by('?')[:20]
    for item in news:
        item.local_img = item.local_img.split('\n')[0]
    context = {
        'news': news,
    }
    return render(request, 'news/homepage.html', context)


def show_list(request, page):
    news = News.objects.order_by('-date')

    # 创建分页器对象，每页显示20个新闻
    paginator = Paginator(news, 20)

    try:
        # 获取指定页数的新闻
        news_page = paginator.page(page)
    except EmptyPage:
        # 如果页数超过范围，返回空页面或其他处理方式
        return HttpResponseRedirect('/news/home')
    for item in news_page:
        item.local_img = item.local_img.split('\n')[0]

    context = {
        'news': news_page,
        'current_page': news_page.number,  # 将当前页数添加到context中
        'total_pages': paginator.num_pages  # 将总页数添加到context中
    }
    return render(request, 'news/list.html', context)


def show_search(request):
    return render(request, 'news/search.html')


def show_search_result(request, page):
    search_request = request.POST.get('searchRequest')  # 获取隐藏字段的值
    if search_request:
        request.session['search_request'] = search_request
    else:
        search_request = request.session.get('search_request')
    search_request = json.loads(search_request)  # 将 JSON 字符串转换为 Python 对象
    query = search_request.get('query')  # 获取搜索关键字
    months = search_request.get('months')  # 获取选中的月份列表
    month_mapping = {
        'checkbox1': 1,
        'checkbox2': 2,
        'checkbox3': 3,
        'checkbox4': 4,
        'checkbox5': 5,
        'checkbox6': 6,
        'checkbox7': 7,
        'checkbox8': 8,
    }
    selected_months = [month_mapping[item] for item in months]
    sort_option = search_request.get('sortOption')  # 获取排序选项
    keys = jieba.lcut(query)

    with open('D:\Program\Python\inverted_index.json', 'r', encoding='utf-8') as f:
        inverted_index = json.load(f)

    if keys:
        news_id_set = set()
        for key in keys:
            pattern = re.compile(re.escape(key), re.IGNORECASE)  # 创建不区分大小写的正则表达式模式
            for inverted_key, news_ids in inverted_index.items():
                if re.search(pattern, inverted_key):
                    news_id_set.update(news_ids)
        news_id_list = list(news_id_set)
        news = News.objects.filter(id__in=news_id_list)
    else:
        news = News.objects.all()
    if selected_months:
        news = news.filter(date__month__in=selected_months)
    if sort_option == 'option1':
        news = news.order_by('-date')
    elif sort_option == 'option2':
        news = news.order_by('-views')
    count = news.count()
    # 创建分页器对象，每页显示20个新闻
    paginator = Paginator(news, 20)

    try:
        # 获取指定页数的新闻
        news_page = paginator.page(page)
    except EmptyPage:
        # 如果页数超过范围，返回空页面或其他处理方式
        return HttpResponseRedirect('/news/home')
    for item in news_page:
        item.local_img = item.local_img.split('\n')[0]

    context = {
        'news': news_page,
        'current_page': news_page.number,  # 将当前页数添加到context中
        'total_pages': paginator.num_pages,  # 将总页数添加到context中
        'query': query,
        'months': months,
        'sortOption': sort_option,
        'count': count,
    }
    return render(request, 'news/search_result.html', context)


def show_mainbody(request, id):
    news = News.objects.get(id=id)
    imgurls = news.local_img.split('\n')
    fmt_date = formats.date_format(news.date, "Y年m月d日 H:i")
    length = len(news.content)
    if length <= 500:
        long = '0-500'
    elif length <= 1000:
        long = '501-1000'
    elif length <= 1500:
        long = '1001-1500'
    elif length <= 2000:
        long = '1501-2000'
    else:
        long = '2000-'
    context = {
        'news': news,
        'imgurls': imgurls,
        'comments': news.comment_set.all(),
        'fmt_date': fmt_date,
        'long': long,
    }
    return render(request, 'news/mainbody.html', context)


def show_classify(request):
    # 获取数据库中的所有新闻数据
    news_list = News.objects.all()

    # 定义分类字典
    classification = {'source': {}, 'dates': {}, 'content_length': {}}

    # 遍历新闻数据，进行分类计数
    for news in news_list:
        # 根据 source 进行分类
        source = news.source
        if source not in classification['source']:
            classification['source'][source] = 0
        classification['source'][source] += 1

        # 根据 date 进行分类 (精确到1-8月)
        month = news.date.month
        if month not in classification['dates']:
            classification['dates'][month] = 0
        classification['dates'][month] += 1

        # 根据 content 长度进行分类
        content_length = len(news.content)
        if content_length <= 500:
            classification['content_length']['0-500'] = classification['content_length'].get(
                '0-500', 0) + 1
        elif content_length <= 1000:
            classification['content_length']['501-1000'] = classification['content_length'].get(
                '501-1000', 0) + 1
        elif content_length <= 1500:
            classification['content_length']['1001-1500'] = classification['content_length'].get(
                '1001-1500', 0) + 1
        elif content_length <= 2000:
            classification['content_length']['1501-2000'] = classification['content_length'].get(
                '1501-2000', 0) + 1
        else:
            classification['content_length']['2000-'] = classification['content_length'].get(
                '2000-', 0) + 1

    return render(request, 'news/classify.html', {'classification': classification})


def show_classify_list(request, species, sort, page):

    if species == "source":
        news = News.objects.filter(source=sort).order_by('-date')
    elif species == "dates":
        news = News.objects.filter(date__month=sort).order_by('-date')
    elif species == "content_length":
        if sort == "0-500":
            news = News.objects.annotate(content_length=Length('content')).filter(
                content_length__gt=0, content_length__lt=501).order_by('-date')
        elif sort == "501-1000":
            news = News.objects.annotate(content_length=Length('content')).filter(
                content_length__gt=500, content_length__lt=1001).order_by('-date')
        elif sort == "1001-1500":
            news = News.objects.annotate(content_length=Length('content')).filter(
                content_length__gt=1000, content_length__lt=1501).order_by('-date')
        elif sort == "1501-2000":
            news = News.objects.annotate(content_length=Length('content')).filter(
                content_length__gt=1500, content_length__lt=2001).order_by('-date')
        elif sort == "2000-":
            news = News.objects.annotate(content_length=Length('content')).filter(
                content_length__gt=2000).order_by('-date')
    # 创建分页器对象，每页显示20个新闻
    paginator = Paginator(news, 20)

    try:
        # 获取指定页数的新闻
        news_page = paginator.page(page)
    except EmptyPage:
        # 如果页数超过范围，返回空页面或其他处理方式
        return HttpResponseRedirect('/news/home')
    for item in news_page:
        item.local_img = item.local_img.split('\n')[0]

    context = {
        'news': news_page,
        'species': species,
        'sort': sort,
        'current_page': news_page.number,  # 将当前页数添加到context中
        'total_pages': paginator.num_pages  # 将总页数添加到context中
    }
    return render(request, 'news/classify_list.html', context)


def comment(request, id):
    data = request.POST
    # 将新的消息添加到数据库中
    user = data['user']
    content = data['content']
    news = News.objects.get(id=id)
    obj = Comment(news=news, user=user, content=content)
    news.comments = F('comments') + 1
    news.save()
    obj.full_clean()  # 对数据进行验证
    obj.save()  # 存储在表中
    return HttpResponseRedirect(f'/news/mainbody/{id}')  # 将页面重定向到博客的url


def delete_comment(request, id, comment_id):
    # 获取要删除的评论对象
    comment = get_object_or_404(Comment, id=comment_id)

    # 获取关联的新闻主体
    news = comment.news

    # 删除评论
    comment.delete()

    # 更新新闻主体的评论计数
    news.comments = F('comments') - 1
    news.save()
    return HttpResponseRedirect(f'/news/mainbody/{id}')  # 将页面重定向到博客的url
