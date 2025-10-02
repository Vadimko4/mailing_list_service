from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from mailer.models import Mailing, Attempt
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Запускает рассылку по указанному ID'

    def add_arguments(self, parser):
        parser.add_argument(
            'mailing_id',
            type=int,
            help='ID рассылки для запуска'
        )

    def handle(self, *args, **options):
        mailing_id = options['mailing_id']

        try:
            mailing = Mailing.objects.get(id=mailing_id)
            self.stdout.write(f"Найдена рассылка: {mailing}")

            # Получаем данные для отправки
            letter_subject = mailing.letter.subject
            letter_content = mailing.letter.content
            recipients_emails = list(mailing.recipients.values_list('email', flat=True))

            self.stdout.write(f"Тема письма: {letter_subject}")
            self.stdout.write(f"Количество получателей: {len(recipients_emails)}")

            if not recipients_emails:
                self.stdout.write(self.style.WARNING("Нет получателей для рассылки"))
                return

            try:
                # Отправка email
                send_mail(
                    subject=letter_subject,
                    message=letter_content,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=recipients_emails,
                    fail_silently=False,
                )

                # Обновляем статус рассылки
                if mailing.status == 'created':
                    mailing.started_at = datetime.now()
                mailing.status = 'started'
                mailing.finished_at = datetime.now()
                mailing.save()

                # Создаем запись об успешной попытке
                Attempt.objects.create(
                    mailing=mailing,
                    status='successfully',
                    date_time=datetime.now(),
                    mail_server_response='Рассылка успешно отправлена через кастомную команду'
                )

                self.stdout.write(
                    self.style.SUCCESS(f"Рассылка {mailing_id} успешно отправлена!")
                )
                self.stdout.write(f"Получатели: {', '.join(recipients_emails)}")

            except Exception as e:
                # Создаем запись о неудачной попытке
                Attempt.objects.create(
                    mailing=mailing,
                    status='unsuccessfully',
                    date_time=datetime.now(),
                    mail_server_response=f'Ошибка: {str(e)}'
                )

                self.stdout.write(
                    self.style.ERROR(f"Ошибка при отправке рассылки: {str(e)}")
                )

        except Mailing.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"Рассылка с ID {mailing_id} не найдена")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Неожиданная ошибка: {str(e)}")
            )
