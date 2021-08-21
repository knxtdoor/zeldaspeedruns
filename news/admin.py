from django.contrib import admin

from news.models import Article


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Article, ArticleAdmin)
