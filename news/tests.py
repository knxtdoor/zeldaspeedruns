from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model

from news.models import Article


class ArticleModelTests(TestCase):
    test_username = 'testuser'
    test_email = 'test@example.com'

    def test_fail_with_no_arguments(self):
        self.assertRaises(
            ValueError,
            Article.objects.create_article,
            title=None,
            content=None,
            author=None,
            pub_date=None
        )

    def test_fail_with_missing_argument(self):
        self.assertRaises(
            ValueError,
            Article.objects.create_article,
            title="Article 1",
            content="This is some content",
            author=None,
            pub_date=timezone.now()
        )

    def test_slug_creation(self):
        u = get_user_model().objects.create_user(
            username=self.test_username, email=self.test_email)
        a = Article.objects.create_article(
            title="Article with many words",
            content="This is some content",
            author=u,
            pub_date=timezone.now()
        )

        self.assertEqual(a.slug, "article-with-many-words")

    def test_date_cant_be_future(self):
        u = get_user_model().objects.create_user(
            username=self.test_username, email=self.test_email)

        self.assertRaises(
            ValueError,
            Article.objects.create_article,
            title="Article 1",
            content="Content",
            author=u,
            pub_date=timezone.now() + timezone.timedelta(days=1)
        )

    def test_markdown_no_formatting(self):
        m = "<p>Content</p>"
        u = get_user_model().objects.create_user(
            username=self.test_username, email=self.test_email)
        a = Article.objects.create_article(
            title="Article 1",
            content="Content",
            author=u,
            pub_date=timezone.now())
        self.assertEqual(m, a.get_content_as_markdown())

    def test_markdown_with_formatting(self):
        m = "<p>Content <em>with</em> <strong>formatting</strong></p>"
        u = get_user_model().objects.create_user(
            username=self.test_username, email=self.test_email)
        a = Article.objects.create_article(
            title="Article 1",
            content="Content *with* **formatting**",
            author=u,
            pub_date=timezone.now())
        self.assertEqual(m, a.get_content_as_markdown())
