from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.template.defaultfilters import striptags, truncatewords_html
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from mptt.fields import TreeForeignKey
from taggit.managers import TaggableManager

from modules.blog.managers import ArticleManager
from modules.system.models import AbstractBaseMeta
from modules.system.services.utils import ImageDirectorySave, unique_slugify, image_optimiser


class Article(AbstractBaseMeta):
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True)
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='articles', verbose_name='Категория')
    short_description = CKEditor5Field(max_length=300, verbose_name='Краткое описание', config_name='extends')
    full_description = CKEditor5Field(verbose_name='Описание', config_name='extends')
    author = models.ForeignKey(
        User, verbose_name='Автор материала',
        on_delete=models.PROTECT,
        related_name='article_author'
    )
    updated_by = models.ForeignKey(User,
                                   verbose_name='Автор обновления',
                                   on_delete=models.PROTECT,
                                   related_name='article_updated_by',
                                   blank=True,
                                   null=True
    )
    created_at = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True, db_index=True)
    reason = models.CharField(verbose_name='Причина обновления', blank=True, max_length=100)
    is_fixed = models.BooleanField(verbose_name='Зафиксировано', default=False, db_index=True)
    is_published = models.BooleanField(verbose_name='Опубликовано', default=True)
    thumbnail = models.ImageField(
        verbose_name='Превью поста',
        blank=True,
        upload_to= ImageDirectorySave('images/thumbnails/'),
        validators=[FileExtensionValidator(
            allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))
        ]
    )
    tags = TaggableManager()
    objects = models.Manager()
    custom = ArticleManager()

    class Meta:
        """
        Сортировка, название модели в админ панели, таблица в данными
        """
        ordering = ('-is_fixed', '-created_at')
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        db_table = 'app_articles'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__thumbnail = self.thumbnail if self.pk else None

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        if not self.meta_title:
            self.meta_title = self.title
        if not self.meta_description:
            self.meta_description = striptags(truncatewords_html(self.short_description, 300))

        super().save(*args, **kwargs)

        if self.__thumbnail != self.thumbnail and self.thumbnail:
            image_optimiser(self.thumbnail.path, height=800, width=800)

    def __str__(self):
        """
        Возвращение строки в виде заголовка статьи
        """
        return self.title

    @property
    def get_thumbnail(self):
        """
        Получение аватара при отсутствии загруженного
        """
        if not self.thumbnail:
            return '/media/images/placeholder.png'
        return self.thumbnail.url

    def get_absolute_url(self):
        """
        Ссылка на статью
        """
        return reverse('article-detail', kwargs={'slug': self.slug})

    def get_rating_sum(self):
        """
        Подсчет рейтинга для статей
        """
        return sum([rating.value for rating in self.article_rating.all()])