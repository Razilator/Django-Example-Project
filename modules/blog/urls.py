from django.urls import path, include

from modules.blog.models import Rating
from modules.blog.views import ArticleListView, ArticleDetailView, ArticleByCategoryListView, ArticleCreateView, \
    ArticleUpdateView, ArticleDeleteView, CommentCreateView, ArticleByTagListView, ArticleSearchResultView, \
    RatingCreateView

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('cat/<int:pk>/<str:slug>/', ArticleByCategoryListView.as_view(), name='article-by-cat'),
    path('articles/', include([
        path('', ArticleListView.as_view(), name='article-list'),
        path('create/', ArticleCreateView.as_view(), name='article-create-view'),
        path('tags/<str:tag>/', ArticleByTagListView.as_view(), name='article-list-by-tags'),
        path('<int:pk>/comments/create/', CommentCreateView.as_view(), name='comment-create-view'),
        path('<str:slug>/', ArticleDetailView.as_view(), name='article-detail'),
        path('<str:slug>/update/', ArticleUpdateView.as_view(), name='article-update-view'),
        path('<str:slug>/delete/', ArticleDeleteView.as_view(), name='article-delete-view'),
        path('<int:pk>/like/', RatingCreateView.as_view(value=Rating.LIKE), name='article-rating-like'),
        path('<int:pk>/dislike/', RatingCreateView.as_view(value=Rating.DISLIKE), name='article-rating-dislike'),
    ])),
    path('search/', ArticleSearchResultView.as_view(), name='search'),

]
