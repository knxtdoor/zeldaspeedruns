from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings


class ArticleManager(models.Manager):
    def create_article(self, title, content, author, pub_date):
        if not title:
            raise ValueError("Title must be supplied")
        if not content:
            raise ValueError("Content must be supplied")
        if not author:
            raise ValueError("Author must be supplied")
        if not pub_date:
            raise ValueError("Publish date must be supplied")
        if pub_date > timezone.now():
            raise ValueError("Cannot be published in the future")

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

    def get_absolute_url(self):
        return reverse('news:article', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
