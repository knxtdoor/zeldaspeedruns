from django.forms import ModelForm
from news.models import Article


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'pub_date']
