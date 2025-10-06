from django.urls import path
from django.contrib.auth import views as auth_views
from users.views import (UserCreateView, email_verification, UserManagementView, toggle_user_active, manager_dashboard,
                         LoginView, RecipientManagementView, MailingManagementView, complete_mailing)
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    # Используем встроенный LoginView
    # path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='users:login'), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('user-management/', UserManagementView.as_view(), name='user_management'),
    path('user-management/toggle-active/<int:user_id>/', toggle_user_active, name='toggle_user_active'),
    path('manager-dashboard/', manager_dashboard, name='manager_dashboard'),
    path('recipient-management/', RecipientManagementView.as_view(), name='recipient_management'),
    path('mailing-management/', MailingManagementView.as_view(), name='mailing_management'),
    path('mailing-management/complete/<int:mailing_id>/', complete_mailing, name='complete_mailing'),
]
