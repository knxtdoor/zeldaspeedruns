from django.urls import path

from . import views

app_name = 'news'
urlpatterns = [
    path('', views.FeedView.as_view(), name="feed"),
    path('article/<slug:slug>/', views.ArticleView.as_view(), name="article"),
]
