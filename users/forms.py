from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import BooleanField

User = get_user_model()


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = "form-check-input"
            else:
                field.widget.attrs['class'] = "form-control"


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")


# class EmailPasswordResetForm(PasswordResetForm):
#     def get_users(self, email):
#         """Найти пользователей по email"""
#         active_users = User.objects.filter(email__iexact=email, is_active=True)
#         return active_users


# class UserLoginForm(StyleFormMixin, AuthenticationForm):
#     class Meta:
#         model = User
#         fields = ("email", "password")
