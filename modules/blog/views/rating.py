from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views import View

from modules.blog.models import Article
from modules.system.services.utils import get_client_ip


class RatingCreateView(View):
    value = None

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def post(self, request, pk):
        if self.is_ajax():
            current_user = request.user
            ip_address = get_client_ip(request)
            article = Article.objects.get(pk=pk)
            if current_user.is_authenticated:
                try:
                    rating = article.article_rating.get(author=current_user)
                    if rating.value is not self.value:
                        rating.value = self.value
                        rating.save(update_fields=['value'])
                    else:
                        rating.delete()
                except ObjectDoesNotExist:
                    article.article_rating.create(author=current_user, value=self.value)
                return JsonResponse({
                    'get_rating_sum': article.get_rating_sum()
                }, status=200)
            else:
                try:
                    rating = article.rating.get(ip_address=ip_address)
                    if rating.value is not self.value:
                        rating.value = self.value
                        rating.save(update_fields=['value'])
                    else:
                        rating.delete()
                except ObjectDoesNotExist:
                    article.article_rating.create(ip_address=ip_address, value=self.value)
                return JsonResponse({
                    'get_rating_sum': article.get_rating_sum()
                }, status=200)
