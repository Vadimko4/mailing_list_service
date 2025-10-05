import secrets
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages import success
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, ListView
from django.contrib import messages
from config.settings import EMAIL_HOST_USER
from mailer.models import Letter, Recipient, Mailing, Attempt
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
            # Q(status='created') | создана, но не запущена - не считаем её активной
            Q(status='started')).count() #запущена - активная
        # То же самое через Q
        # active_mailings_count = Mailing.objects.filter(
        #     Q(owner=user) & (Q(status='created') | Q(status='started'))
        # ).count()
        attempt_count = Attempt.objects.count()
        successfull_attempt_count = Attempt.objects.filter(status='successfully').count()
        effectiveness = int(successfull_attempt_count / attempt_count * 100)
        context.update({
            'letters_count': letters_count,
            'recipients_count': recipients_count,
            'mailings_count': mailings_count,
            'active_mailings_count': active_mailings_count,
            'attempt_count': attempt_count,
            'successfull_attempt_count': successfull_attempt_count,
            'effectiveness': effectiveness
        })
        return context


class UserManagementView(PermissionRequiredMixin, ListView):
    """View для отображения списка пользователей"""
    model = User
    template_name = 'users/user_management.html'
    context_object_name = 'users'
    permission_required = 'users.can_toggle_user_active'
    login_url = '/users/login/'

    def get_queryset(self):
        # Исключаем текущего пользователя и суперпользователей из списка
        return User.objects.exclude(id=self.request.user.id).exclude(is_superuser=True)


@permission_required('users.can_toggle_user_active', login_url='/users/login/')
def toggle_user_active(request, user_id):
    """View для блокировки/разблокировки пользователя"""
    if request.method == 'POST':
        try:
            user = get_object_or_404(User, id=user_id)

            # Не позволяем менять свой статус
            if user.id == request.user.id:
                messages.error(request, 'Вы не можете изменить свой статус')
                return redirect('users:user_management')

            # Не позволяем менять статус суперпользователей
            if user.is_superuser:
                messages.error(request, 'Вы не можете изменять статус суперпользователя')
                return redirect('users:user_management')

            # Меняем статус
            user.is_active = not user.is_active
            user.save()

            action = "разблокирован" if user.is_active else "заблокирован"
            messages.success(request, f'Пользователь {user.email} {action}')

        except User.DoesNotExist:
            messages.error(request, 'Пользователь не найден')

    return redirect('users:user_management')


@permission_required('users.can_toggle_user_active', login_url='/users/login/')
def manager_dashboard(request):
    """Dashboard для менеджера"""
    active_users_count = User.objects.filter(is_active=True).exclude(is_superuser=True).count()
    inactive_users_count = User.objects.filter(is_active=False).exclude(is_superuser=True).count()

    return render(request, 'users/manager_dashboard.html', {
        'active_users_count': active_users_count,
        'inactive_users_count': inactive_users_count,
    })


class LoginView(AuthLoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        # Проверяем, есть ли у пользователя право can_toggle_user_active
        if self.request.user.has_perm('users.can_toggle_user_active'):
            return reverse_lazy('users:manager_dashboard')
        else:
            return reverse_lazy('home')
