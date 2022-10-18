# Generated by Django 4.1 on 2022-09-16 05:39

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_article_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='full_description',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='article',
            name='short_description',
            field=django_ckeditor_5.fields.CKEditor5Field(max_length=300, verbose_name='Краткое описание'),
        ),
    ]