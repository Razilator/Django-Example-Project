from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from modules.blog.models import Article, Category, Comment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author')
    list_display_links = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """
    Админ-панель модели категорий
    """
    list_display = ('tree_actions', 'indented_title', 'id', 'title', 'slug')
    list_display_links = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        ('Основная информация', {'fields': ('title', 'slug', 'parent')}),
        ('Описание', {'fields': ('description',)}),
    )


@admin.register(Comment)
class CommentAdminPage(DraggableMPTTAdmin):
    """
    Админ-панель модели комментариев
    """
    list_display = ('tree_actions', 'indented_title', 'article', 'author', 'created_at', 'is_published')
    mptt_level_indent = 2
    list_display_links = ('article',)
    list_filter = ('created_at', 'is_fixed', 'author')
    list_editable = ('is_published',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'article')