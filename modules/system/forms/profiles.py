from django import forms
from django.contrib.auth.models import User

from modules.system.models import Profile


class ProfileUpdateForm(forms.ModelForm):
    """
    Форма обновления данных профиля пользователя
    """
    class Meta:
        model = Profile
        fields = ('slug', 'bio', 'avatar', 'date_birthday')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы обновления
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class UserUpdateForm(forms.ModelForm):
    """
    Форма обновления данных пользователя
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы обновления
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    def clean_email(self):
        """
        Проверка email на уникальность
        """
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email адрес должен быть уникальным')
        return email