from datetime import date, timedelta

from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from modules.system.services.utils import ImageDirectorySave, unique_slugify, image_optimiser


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='Профиль пользователя', on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name='Персональная ссылка', max_length=255, blank=True, unique=True)
    bio = models.TextField(max_length=500, verbose_name='Информация о себе', blank=True)
    avatar = models.ImageField(
        verbose_name='Аватар профиля',
        blank=True,
        upload_to=ImageDirectorySave('images/avatars/'),
        validators=[FileExtensionValidator(
            allowed_extensions=('png', 'jpg', 'webp', 'jpeg'))
        ]
    )
    date_birthday = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    following = models.ManyToManyField('self', verbose_name='Подписки', related_name='followers', symmetrical=False, blank=True)

    class Meta:
        """
        Сортировка, название модели в админ панели, таблица в данными
        """
        ordering = ('user',)
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили пользователей'
        db_table = 'app_profiles'

    def save(self, *args, **kwargs):
        """
        Сохранение параметров модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.user.username)
        if self.slug:
            self.slug = self.slug.lower()
        super().save(*args, **kwargs)

        if self.avatar:
            image_optimiser(self.avatar.path, height=300, width=300)

    def __str__(self):
        """
        Возвращение имени пользователя
        """
        return self.user.username

    @property
    def get_avatar(self):
        """
        Получение аватара при отсутствии загруженного
        """
        if not self.avatar:
            return f'https://ui-avatars.com/api/?size=128&background=random&name={self.user.username}'
        return self.avatar.url

    @property
    def get_age(self):
        """
        Вычисление возраста пользователя
        """
        if self.date_birthday:
            return (date.today() - self.date_birthday) // timedelta(days=365.2425)
        return 'не указан'

    def is_online(self):
        """
        Показывает данные об онлайне
        """
        if self.user.last_login:
            now = timezone.now()
            if now > self.user.last_login + timezone.timedelta(seconds=300):
                return False
            return True
        else:
            return False

    def get_absolute_url(self):
        """
        Ссылка на профиль
        """
        return reverse('profile', kwargs={'slug': self.slug})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Сигнал создания профиля пользователя
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Сигнал пересохранения профиля пользователя
    """
    instance.profile.save()