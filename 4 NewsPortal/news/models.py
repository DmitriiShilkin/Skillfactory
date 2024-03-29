import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
# импортируем кэш
from django.core.cache import cache

# Create your models here.

article = 'AR'
news = 'NS'

ART_NEWS = [
    (article, 'Статья'),
    (news, 'Новость')
]


class Author(models.Model):
    author_rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        # get all author's posts
        a_posts = Post.objects.filter(author_id=self.pk)
        # summarize all author's posts ratings and get the value from the dictionary by the key
        a_posts_total_rating = a_posts.aggregate(Sum('post_rating'))['post_rating__sum']

        # get all author's comments
        a_comments = Comment.objects.filter(user_id=self.user)
        # summarize all author's comments ratings and get the value from the dictionary by the key
        a_comments_total_rating = a_comments.aggregate(Sum('comment_rating'))['comment_rating__sum']

        # get all users' comments to author's posts
        u_comments = Comment.objects.filter(post__author=self)
        # summarize all users' comments ratings to author's posts and get the value from the dictionary by the key
        u_comments_total_rating = u_comments.aggregate(Sum('comment_rating'))['comment_rating__sum']

        self.author_rating = a_posts_total_rating * 3 + a_comments_total_rating + u_comments_total_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    news_type = models.CharField(max_length=2, choices=ART_NEWS, default=news)
    datetime_in = models.DateTimeField(auto_now_add=True)
    headline = models.CharField(max_length=128)
    content = models.TextField()
    post_rating = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory', related_name='post')

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        if self.post_rating > 0:
            self.post_rating -= 1
        else:
            self.post_rating = 0
        self.save()

    def preview(self):
        return self.content[:124] + '...'

    # def __str__(self):
    #     return f'{self.headline.title()}: {self.content[:20]}'

    # функция reverse позволяет нам указывать не путь вида /news/…, а название пути, которое мы задали в файле urls.py
    # для аргумента name
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    # при изменении объекта будем удалять его из кэша
    def save(self, *args, **kwargs):
        # сначала вызываем метод родителя, чтобы объект сохранился
        super().save(*args, *kwargs)
        # затем удаляем его из кэша, чтобы сбросить pk
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.CharField(max_length=255, blank=True)
    datetime_on = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        if self.comment_rating > 0:
            self.comment_rating -= 1
        else:
            self.comment_rating = 0
        self.save()


def get_current_day():
    now = datetime.datetime.now()
    today = now.replace(hour=0, minute=0, second=0)
    tomorrow = today + datetime.timedelta(days=1)
    return today, tomorrow
