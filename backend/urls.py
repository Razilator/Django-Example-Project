from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap

from django.conf.urls.static import static
from backend import settings
from modules.blog.feeds import LatestArticlesFeed
from modules.blog.sitemaps import ArticleSitemap

handler403 = 'modules.system.views.tr_handler403'
handler404 = 'modules.system.views.tr_handler404'
handler500 = 'modules.system.views.tr_handler500'

sitemaps = {
    'articles': ArticleSitemap,
}

urlpatterns = [
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('admin/', admin.site.urls),
    path('s/', include('modules.system.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('feed/', LatestArticlesFeed()),
    path('', include('modules.blog.urls')),
]

if settings.DEBUG:
    urlpatterns = [path('__debug__/', include('debug_toolbar.urls'))] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)