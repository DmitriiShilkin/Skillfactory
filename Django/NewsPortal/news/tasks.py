import datetime

from django.conf import settings
from django.template.loader import render_to_string
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives
from .models import Post, Category


# наша задача по еженедельной отправке сообщения подписчикам со списком новых публикаций за неделю
# из категорий, на которые они подписаны
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


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
