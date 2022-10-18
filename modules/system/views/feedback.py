from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from modules.system.forms.feedback import CreateFeedbackForm
from modules.system.models import Feedback
from modules.system.services.email import send_contact_email_message
from modules.system.services.utils import get_client_ip


class FeedbackCreateView(SuccessMessageMixin, CreateView):
    model = Feedback
    form_class = CreateFeedbackForm
    success_message = 'Ваше письмо успешно отправлено администрации сайта'
    template_name = 'modules/system/feedback/feedback.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контактная форма'
        return context

    def form_valid(self, form):
        current_user = self.request.user
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.ip_address = get_client_ip(self.request)
            if current_user.is_authenticated:
                feedback.user = current_user
            user_id = getattr(feedback, 'user_id', None)
            send_contact_email_message(feedback.subject, feedback.email, feedback.content, feedback.ip_address, user_id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')