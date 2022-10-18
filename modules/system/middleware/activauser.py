from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class ActiveUserMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.session.session_key:
            cache_key = f'last-seen-{request.session.session_key}'
            last_login = cache.get(cache_key)

            if not last_login and request.user.is_authenticated:
                User.objects.filter(id=request.user.id).update(last_login=timezone.now())
                visit_time = 300
                cache.set(cache_key, 1, visit_time)