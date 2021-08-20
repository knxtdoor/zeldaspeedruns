from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Article
# Create your views here.


class FeedView(ListView):
    template_name = 'news/feed.html'

    def get_queryset(self):
        return Article.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


class ArticleView(DetailView):
    model = Article
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    template_name = 'news/article.html'
