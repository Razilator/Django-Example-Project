import random

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from taggit.models import Tag

from modules.blog.forms import ArticleCreateForm, CommentCreateForm
from modules.blog.forms.articles import ArticleUpdateForm
from modules.blog.models import Article, Category
from modules.blog.services import AuthorRequiredMixin


class ArticleSearchResultView(ListView):
    """
    Реализация поиска статей на сайте
    """
    model = Article
    context_object_name = 'articles'
    paginate_by = 10
    allow_empty = True
    template_name = 'modules/blog/articles/article-list.html'

    def get_queryset(self):
        query = self.request.GET.get('do')
        search_vector = SearchVector('full_description', weight='B') + SearchVector('title', weight='A')
        search_query = SearchQuery(query)
        return (
            self.model.objects.annotate(rank=SearchRank(search_vector, search_query))
                .filter(rank__gte=0.3)
                .order_by('-rank')
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Результаты поиска'
        context['do'] = f"do={self.request.GET.get('value')}&"
        return context


class ArticleListView(ListView):
    model = Article
    template_name = 'modules/blog/articles/article-list.html'
    context_object_name = 'articles'
    paginate_by = 10
    queryset = Article.custom.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context


class ArticleDetailView(DetailView):
    """
    Представление детальной статьи
    """
    model = Article
    template_name = 'modules/blog/articles/article-detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        queryset = Article.custom.detail()
        return queryset

    @staticmethod
    def get_similar_articles(obj):
        article_tags_ids = obj.tags.values_list('id', flat=True)
        similar_articles = Article.objects.filter(tags__in=article_tags_ids).exclude(id=obj.id)
        similar_articles = similar_articles.annotate(related_tags=Count('tags')).order_by('-related_tags')
        similar_articles_list = [similar for similar in similar_articles.all()]
        random.shuffle(similar_articles_list)
        return similar_articles_list[0:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object.title}'
        context['form'] = CommentCreateForm
        context['similar_articles'] = self.get_similar_articles(self.object)
        return context


class ArticleByCategoryListView(ListView):
    model = Article
    template_name = 'modules/blog/articles/article-list.html'
    context_object_name = 'articles'
    category = None
    queryset = Article.custom.all()

    def get_queryset(self):
        self.category = Category.objects.get(pk=self.kwargs['pk'])
        queryset = self.queryset.filter(category_id=self.category.id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Статьи из категории: {self.category.title}'
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """
    Представление: создание материалов на сайте
    """
    model = Article
    template_name = 'modules/blog/articles/article-create.html'
    form_class = ArticleCreateForm
    login_url = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи на сайт'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class ArticleUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: обновления материала на сайте
    """
    model = Article
    template_name = 'modules/blog/articles/article-update.html'
    context_object_name = 'article'
    form_class = ArticleUpdateForm
    login_url = 'home'
    success_message = 'Вы успешно обновили статью'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление статьи: {self.object.title}'
        return context


class ArticleDeleteView(AuthorRequiredMixin, DeleteView):
    """
    Представление: удаления материала
    """
    model = Article
    success_url = reverse_lazy('article-list')
    context_object_name = 'article'
    template_name = 'modules/blog/articles/article-delete.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление статьи: {self.object.title}'
        return context


class ArticleByTagListView(ListView):
    model = Article
    template_name = 'modules/blog/articles/article-list.html'
    context_object_name = 'articles'
    paginate_by = 10
    tag = None

    def get_queryset(self):
        self.tag = Tag.objects.get(slug=self.kwargs['tag'])
        queryset = Article.objects.all().filter(tags__slug=self.tag.slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Статьи по тегу: {self.tag.name}'
        return context