"""zeldaspeedruns URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from news.views import ArticleListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth2/', include('oauth2_provider.urls',
                            namespace='oauth2_provider')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('auth/', include('social_django.urls', namespace='social')),
    path('api-auth/', include('rest_framework.urls')),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

urlpatterns += i18n_patterns(
    path('', ArticleListView.as_view(), name='index'),
    path('news/', include('news.urls', namespace='news')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
)
