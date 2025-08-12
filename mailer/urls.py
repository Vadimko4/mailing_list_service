from django.urls import path

from mailer.apps import MailerConfig
from django.views.decorators.cache import cache_page

from mailer.views import LetterListView, LetterDetailView, LetterCreateView, LetterDeleteView, LetterUpdateView

app_name = MailerConfig.name

urlpatterns = [
    path('letters/<int:pk>/', cache_page(60)(LetterListView.as_view()), name='letter_list'),
    # path('contacts/', ContactsView.as_view(), name='contacts'),
    path('letters/detail/<int:pk>/', LetterDetailView.as_view(), name='letter_detail'),
    path('letters/create/', LetterCreateView.as_view(), name='letter_create'),
    path('letters/update/<int:pk>/', LetterUpdateView.as_view(), name='letter_update'),
    path('letters/delete/<int:pk>/', LetterDeleteView.as_view(), name='letter_delete'),
    # path('categories/<int:pk>/', cache_page(60)(CategoryDetailView.as_view()), name='category_detail'),
]
