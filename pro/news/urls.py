from django.urls import path, include
import news.views as views

urlpatterns = [
    path('home', views.show_home),
    path('classify', views.show_classify),
    path('search', views.show_search),
    path('search/result/<int:page>',views.show_search_result, name='show_search_result'),
    path('classify/<str:species>/<str:sort>/<int:page>',
         views.show_classify_list, name='show_classify_list'),
    path('list/<int:page>', views.show_list),
    path('mainbody/<int:id>', views.show_mainbody),
    path('mainbody/<int:id>/', views.comment, name='comment'),
    path('mainbody/<int:id>/<int:comment_id>/',
         views.delete_comment, name='delete_comment'),
]
