from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView, \
    LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView

from modules.system.forms.authenticated import UserRegisterForm, UserLoginForm, UserPasswordChangeForm, \
    UserForgotPasswordForm, UserSetNewPasswordForm
from modules.system.services.utils import account_activation_token
from modules.system.services.tasks import send_activate_email_task


class RegisterCreateView(SuccessMessageMixin, CreateView):
    """
    Представление регистрации на сайте с формой регистрации
    """
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    template_name = 'modules/system/authenticated/register.html'
    success_message = 'Вы успешно зарегистрировались. Подтвердите ваш email адрес. Может попасть в папку СПАМ!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_activate_email_task.delay(user.email)
        return super().form_valid(form)


class UserLoginView(SuccessMessageMixin, LoginView):
    """
    Авторизация на сайте
    """
    form_class = UserLoginForm
    template_name = 'modules/system/authenticated/login.html'
    next_page = 'home'
    success_message = 'Добро пожаловать на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация на сайте'
        return context


class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    """
    Изменение пароля пользователя
    """
    form_class = UserPasswordChangeForm
    template_name = 'modules/system/authenticated/password-change.html'
    success_message = 'Ваш пароль был успешно изменён!'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение пароля на сайте'
        return context

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'slug': self.request.user.profile.slug})


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Представление по сбросу пароля по почте
    """
    form_class = UserForgotPasswordForm
    template_name = 'modules/system/authenticated/password-reset.html'
    success_url = reverse_lazy('home')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлено на ваш email'
    subject_template_name = 'modules/system/authenticated/email/password-subject-reset-mail.html'
    email_template_name = 'modules/system/authenticated/email/password-reset-mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Сброс пароля на сайте'
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """
    Представление установки нового пароля
    """
    form_class = UserSetNewPasswordForm
    template_name = 'modules/system/authenticated/password-set-new.html'
    success_url = reverse_lazy('home')
    success_message = 'Вы успешно восстановили пароль, теперь вы можете авторизоваться с новым паролем'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
        return context


class UserLogoutView(LogoutView):
    """
    Выход с сайта
    """
    next_page = 'home'


class ActivateAccountView(View):
    """
    Активация аккаунта на сайте по токену
    """

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, 'Ваш аккаунт успешно подтвержден')
            return redirect('home')
        else:
            messages.warning(request, 'Ссылка на активацию аккаунта устарела или не работает')
            return redirect('home')