from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from users.views import IndexView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', IndexView.as_view(), name='home'),
                  path('mailer/', include('mailer.urls', namespace='mailer')),
                  path('users/', include('users.urls', namespace='users')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
