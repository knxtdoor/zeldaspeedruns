from django.urls import path

from news import views

app_name = 'news'
urlpatterns = [
    path('', views.ArticleListView.as_view(), name='feed'),
    path('new/', views.ArticleCreateView.as_view()),
    path('article/<slug:slug>/', views.ArticleDetailView.as_view(),
         name='article'),
]
