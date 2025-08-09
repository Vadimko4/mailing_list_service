from django.contrib import admin

from mailer.models import Letter


@admin.register(Letter)  # Регистрируем модель
class LetterAdmin(admin.ModelAdmin):
    # Настраиваем поля, которые будем выводить в админке
    list_display = ('id', 'subject',)
