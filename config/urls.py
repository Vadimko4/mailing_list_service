from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from users.views import IndexView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', IndexView.as_view(), name='home'),
                  path('mailer/', include('mailer.urls', namespace='mailer')),

                  # URLs восстановления пароля БЕЗ пространства имен
                  path('password-reset/',
                       auth_views.PasswordResetView.as_view(
                           template_name='users/password_reset.html'
                       ),
                       name='password_reset'),
                  path('password-reset/done/',
                       auth_views.PasswordResetDoneView.as_view(
                           template_name='users/password_reset_done.html'
                       ),
                       name='password_reset_done'),
                  path('password-reset-confirm/<uidb64>/<token>/',
                       auth_views.PasswordResetConfirmView.as_view(
                           template_name='users/password_reset_confirm.html'
                       ),
                       name='password_reset_confirm'),
                  path('password-reset-complete/',
                       auth_views.PasswordResetCompleteView.as_view(
                           template_name='users/password_reset_complete.html'
                       ),
                       name='password_reset_complete'),

                  # Остальные URLs приложения users с пространством имен
                  path('users/', include('users.urls', namespace='users')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
