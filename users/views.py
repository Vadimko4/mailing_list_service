import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView

from config.settings import EMAIL_HOST_USER
from mailer.models import Letter, Recipient, Mailing
from users.forms import UserRegisterForm
from users.models import User
from django.db.models import Q


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Здравствуйте, перейдите по ссылке для подтверждения Вашей почты: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        letters_count = Letter.objects.filter(owner=user).count()
        recipients_count = Recipient.objects.filter(owner=user).count()
        mailings_count = Mailing.objects.filter(owner=user).count()
        active_mailings_count = Mailing.objects.filter(owner=user).filter(
            Q(status='created') | Q(status='started')).count()
        # То же самое через Q
        # active_mailings_count = Mailing.objects.filter(
        #     Q(owner=user) & (Q(status='created') | Q(status='started'))
        # ).count()
        context.update({
            'letters_count': letters_count,
            'recipients_count': recipients_count,
            'mailings_count': mailings_count,
            'active_mailings_count': active_mailings_count,
        })
        return context
