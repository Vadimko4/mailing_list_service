from django.urls import path
from django.contrib.auth import views as auth_views
from users.views import UserCreateView, email_verification
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    # Используем встроенный LoginView
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='users:login'), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
]
