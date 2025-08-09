from django.db import models

from users.models import User


class Letter(models.Model):
    subject = models.CharField(max_length=150, verbose_name='Тема письма', help_text='Введите тему письма')
    content = models.TextField(verbose_name='Текст письма',
                                   help_text='Введите текст письма',default='отсутствует')
    owner = models.ForeignKey(User, verbose_name="Владелец", help_text="Укажите владельца письма", blank=True,
                              null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'
        ordering = ['owner', 'subject']
        # permissions = [
        #     ("can_unpublish_product", "can unpublish product"),
        # ]
