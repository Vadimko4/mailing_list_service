from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(upload_to="users/avatars/", verbose_name="Аватар", blank=True, null=True,
                               help_text="Загрузите свой аватар")
    phone = models.CharField(max_length=15, verbose_name="Телефон", blank=True, null=True,
                             help_text="Введите номер телефона")
    country = models.CharField(max_length=50, verbose_name="Страна", blank=True, null=True,
                             help_text="Введите страну")

    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)

    USERNAME_FIELD = "email" # меняем юзернейм на почту
    REQUIRED_FIELDS = ['username',]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ("can_toggle_user_active", "Может блокировать/разблокировать пользователя"),
        ]

    def __str__(self):
        return self.email

    # Автоматически в поле username сохраняем email, иначе будет оставаться пустым и при создании новых пользователей
    # будет ругаться, что пользователь с таким именем уже есть
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
