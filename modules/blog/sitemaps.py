from django.contrib.sitemaps import Sitemap

from modules.blog.models import Article


class ArticleSitemap(Sitemap):
    """
    Sitemap для статей
    """
    changefreq = 'monthly'
    priority = 0.9
    i18n = False
    alternates = True
    protocol = 'https'

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.created_at