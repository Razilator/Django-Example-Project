from django.db import models


class AbstractBaseMeta(models.Model):
    """
    Мета теги для обработки SEO в моделях, чтобы продвигать статьи в поисковике
    """
    meta_title = models.CharField(verbose_name='Мета-название', max_length=255, blank=True)
    meta_description = models.CharField(verbose_name='Мета-описание', blank=True, max_length=300)
    meta_keywords = models.CharField(verbose_name='Ключевые слова', max_length=255, blank=True)

    class Meta:
        abstract = True