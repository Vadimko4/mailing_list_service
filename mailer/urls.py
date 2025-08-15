from django.urls import path

from mailer.apps import MailerConfig
from django.views.decorators.cache import cache_page

from mailer.views import LetterListView, LetterDetailView, LetterCreateView, LetterDeleteView, LetterUpdateView, \
    RecipientListView, RecipientDetailView, RecipientCreateView, RecipientDeleteView, RecipientUpdateView

app_name = MailerConfig.name

urlpatterns = [
    path('letters/<int:pk>/', cache_page(60)(LetterListView.as_view()), name='letter_list'),
    path('recipients/<int:pk>/', RecipientListView.as_view(), name='recipient_list'),
    path('letters/detail/<int:pk>/', LetterDetailView.as_view(), name='letter_detail'),
    path('recipients/detail/<int:pk>/', RecipientDetailView.as_view(), name='recipient_detail'),
    path('letters/create/', LetterCreateView.as_view(), name='letter_create'),
    path('recipients/create/', RecipientCreateView.as_view(), name='recipient_create'),
    path('letters/update/<int:pk>/', LetterUpdateView.as_view(), name='letter_update'),
    path('recipient/update/<int:pk>/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('letters/delete/<int:pk>/', LetterDeleteView.as_view(), name='letter_delete'),
    path('recipient/delete/<int:pk>/', RecipientDeleteView.as_view(), name='recipient_delete'),
]
