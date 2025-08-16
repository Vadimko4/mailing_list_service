from django.urls import path

from mailer.apps import MailerConfig
from django.views.decorators.cache import cache_page

from mailer.views import LetterListView, LetterDetailView, LetterCreateView, LetterDeleteView, LetterUpdateView, \
    RecipientListView, RecipientDetailView, RecipientCreateView, RecipientDeleteView, RecipientUpdateView, \
    MailingListView, MailingDetailView, MailingCreateView, MailingDeleteView, MailingUpdateView, SendMailView

app_name = MailerConfig.name

urlpatterns = [
    path('letters/<int:pk>/', cache_page(60)(LetterListView.as_view()), name='letter_list'),
    path('letters/detail/<int:pk>/', LetterDetailView.as_view(), name='letter_detail'),
    path('letters/create/', LetterCreateView.as_view(), name='letter_create'),
    path('letters/update/<int:pk>/', LetterUpdateView.as_view(), name='letter_update'),
    path('letters/delete/<int:pk>/', LetterDeleteView.as_view(), name='letter_delete'),
    path('recipients/<int:pk>/', RecipientListView.as_view(), name='recipient_list'),
    path('recipients/detail/<int:pk>/', RecipientDetailView.as_view(), name='recipient_detail'),
    path('recipients/create/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipient/update/<int:pk>/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipient/delete/<int:pk>/', RecipientDeleteView.as_view(), name='recipient_delete'),
    path('mailings/<int:pk>/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('send_mail/<int:pk>/', SendMailView.as_view(), name='send_mail'),
]
