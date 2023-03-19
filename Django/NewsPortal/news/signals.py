from django.conf import settings
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from .models import PostCategory


def send_mails(preview, pk, headline, subscribers_emails):
    # указываем какой шаблон брать за основу и преобразовываем его в строку для отправки подписчику
    html_context = render_to_string(
        'mail/post_add_email.html',
        {
            'content': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        # тема письма
        subject=headline,
        # тело пустое, потому что мы используем шаблон
        body='',
        # адрес отправителя
        from_email=settings.DEFAULT_FROM_EMAIL,
        # список адресатов
        to=subscribers_emails,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send(fail_silently=False)


@receiver(m2m_changed, sender=PostCategory)
def post_add_notification(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers = []
        subscribers_emails = []
        for category in categories:
            subscribers += category.subscribers.all()

        for s in subscribers:
            subscribers_emails.append(s.email)

        send_mails(instance.preview(), instance.pk, instance.headline, subscribers_emails)
