from django.db import models

from users.models import User


class Letter(models.Model):
    subject = models.CharField(max_length=150, verbose_name='Тема письма', help_text='Введите тему письма')
    content = models.TextField(verbose_name='Текст письма',
                               help_text='Введите текст письма', default='отсутствует')
    owner = models.ForeignKey(User, verbose_name="Владелец", help_text="Укажите владельца письма", blank=True,
                              null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'
        ordering = ['owner', 'subject']
        # permissions = [
        #     ("can_unpublish_product", "can unpublish product"),
        # ]

    def __str__(self):
        return self.subject


class Recipient(models.Model):
    email = models.EmailField(blank=False, null=False, verbose_name="Email", help_text='Введите email')
    fio = models.CharField(max_length=150, verbose_name="ФИО", blank=True, null=True,
                           help_text="Введите ФИО")
    comment = models.TextField(verbose_name='Комментарий', help_text='Введите комментарий', default='отсутствует')
    owner = models.ForeignKey(User, verbose_name="Владелец", help_text="Укажите владельца получателя", blank=True,
                              null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'
        ordering = ['owner', 'email', 'fio']

    def __str__(self):
        return self.email


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    started_at = models.DateTimeField(blank=True, null=True, verbose_name='Дата и время первой отправки',
                                      help_text='Укажите дату и время первой отправки')
    finished_at = models.DateTimeField(blank=True, null=True, verbose_name='Дата и время первой отправки',
                                       help_text='Укажите дату и время первой отправки')
    letter = models.ForeignKey(Letter, verbose_name="Сообщение", help_text="Укажите сообщение для рассылки",
                               blank=False, null=False, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient, related_name='mailings', verbose_name="Получатели",
                                        help_text="Укажите получателей рассылки")
    owner = models.ForeignKey(User, verbose_name="Владелец", help_text="Укажите владельца рассылки", blank=False,
                              null=False, on_delete=models.CASCADE)

    def get_status_display(self):
        return dict(self.STATUS_CHOICES)[self.status]

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['status','owner', 'started_at', 'finished_at']

    def __str__(self):
        return f"mailing id: {self.id}; letter subject: {self.letter.subject}; mailing status: {self.status}"
