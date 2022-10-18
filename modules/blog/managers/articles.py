from django.db import models


class ArticleManager(models.Manager):
    """
    Кастомный менеджер для модели статей.
    """

    def all(self):
        """
        Список статей (SQL запрос с фильтрацией для страницы списка статей)
        """
        return self.get_queryset().filter(is_published=True).select_related('category').prefetch_related('article_rating')

    def detail(self):
        """
        Детальная страница статьи с оптимизацией
        """
        return self.get_queryset().filter(is_published=True)\
            .select_related('category', 'updated_by', 'author', 'author__profile')\
            .prefetch_related('comments', 'comments__author', 'comments__author__profile')