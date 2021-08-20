from django.db import models
from django.utils.text import slugify
from django.utils import timezone


from zeldaspeedruns import settings

# Create your models here.


class ArticleManager(models.Manager):
    def create_article(self, title, content, author, pub_date):
        if not title or not content or not author or not pub_date:
            raise ValueError("Invalid article parameters")
        if pub_date > timezone.now():
            raise ValueError("Cannot be published in the future!")
        article = self.model(
            title=title,
            content=content,
            author=author,
            pub_date=pub_date,
            slug=(slugify(title))
        )
        article.save()
        return article


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    slug = models.SlugField(unique=True)
    objects = ArticleManager()

    def __str__(self):
        return self.title
