import datetime

from celery import shared_task

from django.conf import settings
from django.template.loader import render_to_string
# используется с apscheduler
# from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives


from .models import Post, Category


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


# задача, которая уведомляет о новой публикации в любимом разделе
@shared_task
def post_add_notification(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    subscribers = []
    subscribers_emails = []
    for category in categories:
        subscribers += category.subscribers.all()

    for s in subscribers:
        subscribers_emails.append(s.email)

    send_mails(post.preview(), post.pk, post.headline, subscribers_emails)


# задача по еженедельной отправке сообщения подписчикам со списком новых публикаций за неделю
# из категорий, на которые они подписаны
@shared_task
def my_job():
    #  Your job processing logic here...
    today = datetime.datetime.now()
    week_ago = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(datetime_in__gte=week_ago)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers_emails = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'mail/weekly_posts.html',
        {
            'link': settings.SITE_URL,
            'posts': posts
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send(fail_silently=False)


# функция, которая будет удалять неактуальные задачи (используется с apscheduler)
def delete_old_job_executions(max_age=604_800):
    pass
#     """This job deletes all apscheduler job executions older than `max_age` from the database."""
#     DjangoJobExecution.objects.delete_old_job_executions(max_age)
