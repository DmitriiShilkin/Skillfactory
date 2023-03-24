from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from .models import Post, Author, Category
from .models import article, news, get_current_day
from .filters import PostFilter
from .forms import PostForm, PostDeleteForm
from .tasks import post_add_notification


# Create your views here.
# Представление для просмотра всех публикаций
class NewsList(ListView):
    model = Post
    ordering = '-datetime_in'
    template_name = 'news/news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


# Представление для просмотра отдельной публикации
class PostDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


# Представление для поиска публикаций
class PostSearch(NewsList):
    template_name = 'news/search.html'
    context_object_name = 'news'
    # Переопределяем функцию получения списка новостей
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список новостей
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


# Представление, создающее новость
class NewsCreate(PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму,
    form_class = PostForm
    # модель новостей,
    model = Post
    # шаблон, в котором используется форма,
    template_name = 'news/news_create.html'
    # и требование права на добавление новости.
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        today, tomorrow = get_current_day()
        author = Author.objects.get(user_id=self.request.user.id)
        posts = Post.objects.filter(author_id=author.pk, datetime_in__gte=today, datetime_in__lt=tomorrow)
        if posts.count() >= 3:
            return redirect('/news/create/error/')

        post = form.save(commit=False)
        post.news_type = news
        post.author = author
        post_add_notification.delay(post.pk)
        return super().form_valid(form)


# Представление, изменяющее новость
class NewsEdit(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'
    # требование права на изменение новости
    permission_required = ('news.change_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_type = news
        return super().form_valid(form)


# Представление, удаляющее новость
class NewsDelete(PermissionRequiredMixin, DeleteView):
    form_class = PostDeleteForm
    model = Post
    template_name = 'news/news_delete.html'
    # требование права на удаление новости
    permission_required = ('news.delete_post',)
    success_url = reverse_lazy('news_list')


# Представление, создающее статью
class ArticleCreate(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/article_create.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        today, tomorrow = get_current_day()
        author = Author.objects.get(user_id=self.request.user.id)
        posts = Post.objects.filter(author_id=author.pk, datetime_in__gte=today, datetime_in__lt=tomorrow)
        if posts.count() >= 3:
            return redirect('/news/create/error/')

        post = form.save(commit=False)
        post.news_type = article
        post.author = author
        post.save()
        post_add_notification.delay(post.pk)
        return super().form_valid(form)


# Представление, изменяющее статью
class ArticleEdit(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/article_edit.html'
    permission_required = ('news.change_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_type = article
        return super().form_valid(form)


# Представление, удаляющее статью
class ArticleDelete(NewsDelete):
    template_name = 'news/article_delete.html'


# Представление, отображающее новости по выбранной категории
class CategoryList(NewsList):
    template_name = 'news/category.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


# Представление для добавления пользователя в группу "Авторы"
@login_required
def make_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        Author.objects.create(user=user)
        authors_group.user_set.add(user)
    return redirect('/news/')


# Представление для подписки на выбранную категорию
@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    is_not_author = not request.user.groups.filter(name='authors').exists()
    data = {'category': category, 'is_not_author': is_not_author}
    return render(request, 'news/subscribe.html', context=data)
