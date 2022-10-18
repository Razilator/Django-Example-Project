from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from modules.blog.models import Article


class Rating(models.Model):
    LIKE = 1
    DISLIKE = -1
    VOTES_TYPE = ((LIKE, _('Нравится')), (DISLIKE, _('Не нравится')))

    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья', related_name='article_rating')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Оценил'), related_name='article_rating_author', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_('Время добавления оценки'), auto_now_add=True, db_index=True)
    value = models.SmallIntegerField(verbose_name=_('Оценка'), choices=VOTES_TYPE)
    ip_address = models.GenericIPAddressField(verbose_name=_('IP Адрес'), blank=True, null=True)

    class Meta:
        """
        Сортировка, название модели в админ панели, таблица в данными
        """
        ordering = ('-created_at',)
        verbose_name = _('Рейтинг материала')
        verbose_name_plural = _('Рейтинг материалов')
        db_table = 'app_ratings'

    def __str__(self):
        if self.author:
            return f'{self.author} поставил {self.get_value_display()} под {self.article.title}'
        return f'Гость: {self.ip_address} поставил {self.get_value_display()} под {self.article.title}'