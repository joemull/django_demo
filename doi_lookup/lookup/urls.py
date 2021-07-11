from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('articles/', views.ArticleListView.as_view(), name = 'articles'),
    path('article/<int:pk>/delete/', views.ArticleDelete.as_view(), name='author-delete'),
    path('articles/<str:given_name>_<str:family_name>/', views.AuthorFilteredArticleListView.as_view(), name = 'author-articles')
]
