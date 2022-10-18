from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms

from backend import settings
from modules.system.models import Feedback


class CreateFeedbackForm(forms.ModelForm):
    """
    Форма отправки обратной связи
    """
    class Meta:
        model = Feedback
        fields = ('subject', 'email', 'content')

    recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, public_key=settings.RECAPTCHA_PUBLIC_KEY, private_key=settings.RECAPTCHA_PRIVATE_KEY, label='Капча')

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