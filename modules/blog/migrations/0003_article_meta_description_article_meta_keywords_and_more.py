# Generated by Django 4.1 on 2022-08-29 15:20

import django.core.validators
from django.db import migrations, models
import modules.system.services.utils


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_category_article_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='meta_description',
            field=models.CharField(blank=True, max_length=300, verbose_name='Мета-описание'),
        ),
        migrations.AddField(
            model_name='article',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=255, verbose_name='Ключевые слова'),
        ),
        migrations.AddField(
            model_name='article',
            name='meta_title',
            field=models.CharField(blank=True, max_length=255, verbose_name='Мета-название'),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_description',
            field=models.CharField(blank=True, max_length=300, verbose_name='Мета-описание'),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=255, verbose_name='Ключевые слова'),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_title',
            field=models.CharField(blank=True, max_length=255, verbose_name='Мета-название'),
        ),
        migrations.AlterField(
            model_name='article',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to=modules.system.services.utils.ImageDirectorySave('images/thumbnails/'), validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))], verbose_name='Превью поста'),
        ),
    ]