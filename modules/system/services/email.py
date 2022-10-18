from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage

from backend import settings
from modules.system.services.utils import account_activation_token


def send_activate_email_message(email):
    user = User.objects.get(email=email)
    current_site = Site.objects.get_current().domain
    subject = 'Активация аккаунта на сайте Django блог'
    message = render_to_string('modules/system/authenticated/email/activate-mail.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    return user.email_user(subject, message)


def send_contact_email_message(subject, email, content, ip, user_id):
    """
    Функция отправки контактной формы
    """
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        user = None
    message = render_to_string('modules/system/feedback/email/contact_mail.html', {
        'email': email,
        'content': content,
        'ip': ip,
        'user': user,
    })
    email = EmailMessage(subject, message, settings.EMAIL_SERVER, settings.EMAIL_ADMIN)
    return email.send(fail_silently=False)