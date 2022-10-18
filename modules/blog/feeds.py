from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from modules.blog.models import Article


class LatestArticlesFeed(Feed):
    title = 'Записки интернет-охотника'
    link = '/articles/'
    description = 'Здесь вы найдете полезные записи интернета'
    language = 'ru'

    def items(self):
        return Article.objects.order_by('-created_at')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.short_description

    def item_link(self, item):
        return reverse('article-detail', args=[item.slug])