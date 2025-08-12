from django.urls import path

from mailer.apps import MailerConfig
from django.views.decorators.cache import cache_page

from mailer.views import LetterListView, LetterCreateView, LetterDeleteView

app_name = MailerConfig.name

urlpatterns = [
    path('letters/<int:pk>/', cache_page(60)(LetterListView.as_view()), name='letter_list'),
    # path('', ProductListView.as_view(), name='home'),
    # path('products/', ProductListView.as_view(), name='home'),
    # path('contacts/', ContactsView.as_view(), name='contacts'),
    # path('products/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('letters/create/', LetterCreateView.as_view(), name='letter_create'),
    # path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('letters/<int:pk>/delete/', LetterDeleteView.as_view(), name='letter_delete'),
    # path('categories/<int:pk>/', cache_page(60)(CategoryDetailView.as_view()), name='category_detail'),
]
