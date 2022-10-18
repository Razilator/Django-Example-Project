from django.contrib.auth.models import User
from django.db import models


class Feedback(models.Model):
    """
    Модель контактной формы
    """
    subject = models.CharField(max_length=255, verbose_name='Тема')
    email = models.EmailField(max_length=255, verbose_name='Email')
    content = models.TextField(verbose_name='Содержимое')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    ip_address = models.GenericIPAddressField(verbose_name='IP Адрес',  blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
        ordering = ('-created_at',)
        db_table = 'app_feedback'

    def __str__(self):
        return f'Вам письмо: {self.email}'