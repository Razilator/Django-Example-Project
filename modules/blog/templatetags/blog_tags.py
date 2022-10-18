from django import template

from modules.blog.models import Article, Comment

register = template.Library()


@register.simple_tag
def total_articles():
    return Article.custom.all().count()


@register.inclusion_tag('includes/tags/last_comments.html')
def show_latest_comments(count=5):
    latest_comments = Comment.objects.all().select_related('author')[:count]
    return {'latest_comments': latest_comments}

