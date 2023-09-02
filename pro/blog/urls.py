from django.urls import path, include
import blog.views as views

urlpatterns = [
    path('blog/<int:id>', views.show_blog),
    path('comment/<int:id>', views.comment)
]