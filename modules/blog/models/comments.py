from django.contrib.auth.models import User
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from modules.blog.models import Article


class Comment(MPTTModel):
    """
    Модель комментариев для блога статей с возможностью вложенности.
    Подключен плагин MPTT для вложенности.
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья', related_name='comments', related_query_name='comment')
    author = models.ForeignKey(User, verbose_name='Автор материала', on_delete=models.CASCADE, related_name='comments_author')
    content = models.TextField(verbose_name='Текст комментария', max_length=1500)
    created_at = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True, db_index=True)
    is_published = models.BooleanField(verbose_name='Опубликовать', default=True)
    is_fixed = models.BooleanField(verbose_name='Зафиксировать', default=False)

    parent = TreeForeignKey('self', verbose_name='Родительский комментарий', null=True, blank=True, db_index=True, related_name='children', on_delete=models.CASCADE)

    class MTTMeta:
        """
        Сортировка по вложенности
        """
        order_insertion_by = ('-created_at',)

    class Meta:
        """
        Сортировка, название модели в админ панели, таблица в данными
        """
        ordering = ('-is_fixed', '-created_at')
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        db_table = 'app_comments'

    def __str__(self):
        """
        Возвращение заголовка статьи
        """
        return f'{self.author} написал под статьей: {self.article.title}'