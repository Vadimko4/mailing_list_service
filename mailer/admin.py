from django.contrib import admin

from mailer.models import Letter, Recipient, Mailing


@admin.register(Letter)  # Регистрируем модель
class LetterAdmin(admin.ModelAdmin):
    # Настраиваем поля, которые будем выводить в админке
    list_display = ('id', 'subject',)


@admin.register(Recipient)  # Регистрируем модель
class RecipientAdmin(admin.ModelAdmin):
    # Настраиваем поля, которые будем выводить в админке
    list_display = ('id', 'email', 'fio','comment')
    # По чему будем делать фильтрацию
    list_filter = ('email', 'fio', 'owner')
    # По чему у нас будет поиск
    search_fields = ('email', 'fio', 'owner')


@admin.register(Mailing)  # Регистрируем модель
class MailingAdmin(admin.ModelAdmin):
    # Настраиваем поля, которые будем выводить в админке
    list_display = ('id', 'status', 'owner', 'letter')
    # По чему будем делать фильтрацию
    list_filter = ('status', 'owner', 'letter')
    # По чему у нас будет поиск
    search_fields = ('id', 'status', 'owner', 'letter')
