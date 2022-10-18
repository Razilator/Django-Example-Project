from django.db import models
from django.template.defaultfilters import striptags, truncatewords_html
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from modules.system.models import AbstractBaseMeta
from modules.system.services.utils import unique_slugify, get_meta_keywords


class Category(MPTTModel, AbstractBaseMeta):
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, verbose_name='URL категории', blank=True)
    description = models.TextField(verbose_name='Описание категории', max_length=300)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name='children',
        verbose_name='Родительская категория'
    )

    class MPTTMeta:
        """
        Сортировка по вложенности
        """
        order_insertion_by = ('title',)

    class Meta:
        """
        Сортировка, название модели в админ панели, таблица в данными
        """
        unique_together = 'parent', 'slug'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'app_categories'

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        if not self.meta_title:
            self.meta_title = self.title
        if not self.meta_description:
            self.meta_description = striptags(truncatewords_html(self.description, 300))
        if not self.meta_keywords:
            self.meta_keywords = get_meta_keywords(self.description)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Возвращение заголовка статьи
        """
        return self.title