import collections
import io
import os
import re
import time
from pathlib import Path
from urllib.parse import urljoin
from uuid import uuid4

import six
from PIL import Image
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.deconstruct import deconstructible
from django.utils.html import strip_tags
from pytils.translit import slugify
from django.core.files.storage import FileSystemStorage

from backend import settings


@deconstructible
class ImageDirectorySave(object):
    """
    Класс загрузчика в определенную директорию
    """
    def __init__(self, save_path):
        self.path = save_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]

        if instance and hasattr(instance, 'slug'):
            filename = f'img-{instance.slug}.{ext}'
        else:
            filename = f'img-{uuid4().hex}.{ext}'
        path = Path(self.path, time.strftime('%Y/%m/%d'), filename)
        return path


def unique_slugify(instance, slug):
    """
    Генератор уникальных SLUG для моделей, в случае существования такого SLUG.
    """
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{unique_slug}-{uuid4().hex[:8]}'
    return unique_slug


def get_meta_keywords(description):
    """
    Генератор meta-keywords из описания статьи
    """
    count_min = 7
    count_length = 7
    collection = collections.Counter()
    content = io.StringIO(description)
    keywords = []
    for line in content.readlines():
        collection.update(re.findall(r"[\w']+", strip_tags(line).lower()))
    for word, count in collection.most_common():
        if len(word) > (count_length - 1) and count > (count_min - 1):
            keywords.append(word)
    return ', '.join(map(str, keywords))


class AppTokenGenerator(PasswordResetTokenGenerator):
    """
    Генерация токенов для регистрации и активации
    """
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.is_active) + six.text_type(user.pk) + six.text_type(timestamp)


account_activation_token = AppTokenGenerator()


def get_client_ip(request):
    """
    Получение IP юзера
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CkeditorCustomStorage(FileSystemStorage):
    """
    Кастомное расположение для медиа файлов
    """
    location = os.path.join(settings.MEDIA_ROOT, 'uploads/images/')
    base_url = urljoin(settings.MEDIA_URL, 'uploads/images/')


def image_optimiser(image_path, height, width):
    """
    Оптимизация изображений
    """
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    if img.height > height or img.width > width:
        output_size = (height, width)
        img.thumbnail(output_size)
    img.save(image_path)