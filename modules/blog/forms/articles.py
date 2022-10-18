from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms

from backend import settings
from modules.blog.models import Article


class ArticleCreateForm(forms.ModelForm):

    """
    Форма добавления статей на сайте
    """
    class Meta:
        model = Article
        fields = (
            'title',
            'slug',
            'category',
            'short_description',
            'full_description',
            'thumbnail',
            'meta_title',
            'meta_keywords',
            'meta_description',
            'is_published',
        )

    recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, public_key=settings.RECAPTCHA_PUBLIC_KEY,
                               private_key=settings.RECAPTCHA_PRIVATE_KEY, label='Капча')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
            self.fields['meta_title'].widget.attrs.update({
                'placeholder': 'Введите мета-название для поисковой системы'
            })
            self.fields['title'].widget.attrs.update({
                'placeholder': 'Заголовок статьи'
            })
            self.fields['slug'].widget.attrs.update({
                'placeholder': 'Ссылка статьи (необязательно)'
            })
            self.fields['meta_description'].widget.attrs.update({
                'placeholder': 'Введите небольшое описание в 300 символов для поисковой системы'
            })
            self.fields['meta_keywords'].widget.attrs.update({
                'placeholder': 'Введите ключевые слова через запятую для поиска'
            })
            self.fields['category'].empty_label = 'Выберите категорию'
            self.fields['is_published'].widget.attrs.update({
                'class': 'form-check-input'
            })
            self.fields['short_description'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
            self.fields['full_description'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
            self.fields['short_description'].required = False
            self.fields['full_description'].required = False


class ArticleUpdateForm(ArticleCreateForm):

    class Meta:
        model = Article
        fields = ArticleCreateForm.Meta.fields + ('reason', 'is_fixed')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        self.fields['is_fixed'].widget.attrs.update({
                'class': 'form-check-input'
        })