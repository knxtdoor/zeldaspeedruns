from django.views.generic import ListView, DetailView
from django.utils import timezone

from news.models import Article


class ArticleListView(ListView):
    template_name = 'news/feed.html'

    def get_queryset(self):
        return Article.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


class ArticleDetailView(DetailView):
    model = Article
    context_object_name = 'article'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    template_name = 'news/article.html'

    def get_object(self):
        obj = super().get_object()
        self.markdown = obj.get_content_as_markdown()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['markdown'] = self.markdown
        return context
