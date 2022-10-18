from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView

from modules.system.forms.profiles import ProfileUpdateForm, UserUpdateForm
from modules.system.models import Profile


class ProfileView(DetailView):
    """
    Представление для показа профиля на страничке
    """
    model = Profile
    context_object_name = 'profile'
    template_name = 'modules/system/profiles/profile-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Страница пользователя: {self.object.user.username}'
        return context


class ProfileEditView(UpdateView):
    """
    Представление для редактирования профиля пользователя.
    """
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'modules/system/profiles/profile-edit.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование профиля пользователя: {self.request.user.username}'
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super(ProfileEditView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'slug': self.object.slug})


class ProfileFollowingCreateView(View):
    """
    Создание подписки для пользователей
    """
    model = Profile

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def post(self, request, slug):
        if self.is_ajax():
            user = self.model.objects.get(slug=slug)
            current_user = request.user
            if current_user.is_authenticated:
                profile = current_user.profile
                if profile in user.followers.all():
                    user.followers.remove(profile)
                    return JsonResponse({
                        'author': current_user.username,
                        'following_avatar': profile.get_avatar,
                        'following_get_absolute_url': profile.get_absolute_url(),
                        'following_slug': profile.slug,
                        'message': f'Подписаться на {user}',
                        'status': False},
                    status=200)
                else:
                    user.followers.add(profile)
                    return JsonResponse({
                        'author': current_user.username,
                        'following_get_absolute_url': profile.get_absolute_url(),
                        'following_slug': profile.slug,
                        'following_avatar': profile.get_avatar,
                        'message': f'Отписаться от {user}',
                        'status': True},
                        status=200)
            else:
                return JsonResponse({'error': 'Необходима авторизация на сайте'}, status=400)
