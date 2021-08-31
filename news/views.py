from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone

from news.models import Article


class ArticleListView(ListView):
    template_name = 'news/feed.html'

    def get_queryset(self):
        return Article.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


class ArticleDetailView(DetailView):
    model = Article
    context_object_name = 'article'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    template_name = 'news/article.html'


class ArticleCreateView(CreateView):
    model = Article
    fields = ['title', 'content', 'pub_date']
    template_name = "news/article_create.html"
