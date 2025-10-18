from django.contrib import admin

from users.models import User


@admin.register(User)  # Регистрируем модель
class UserAdmin(admin.ModelAdmin):
    # Настраиваем поля, которые будем выводить в админке
    list_display = ('id', 'email',)
