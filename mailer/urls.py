from django.urls import path

from mailer.apps import MailerConfig
from django.views.decorators.cache import cache_page

from mailer.views import LetterListView

app_name = MailerConfig.name

urlpatterns = [
    path('letters/<int:pk>/', cache_page(60)(LetterListView.as_view()), name='letter_list'),
    # path('', ProductListView.as_view(), name='home'),
    # path('products/', ProductListView.as_view(), name='home'),
    # path('contacts/', ContactsView.as_view(), name='contacts'),
    # path('products/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    # path('products/create/', ProductCreateView.as_view(), name='product_create'),
    # path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    # path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    # path('categories/<int:pk>/', cache_page(60)(CategoryDetailView.as_view()), name='category_detail'),
]
