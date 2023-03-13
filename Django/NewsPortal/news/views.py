# from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from .models import Post, Author
from .models import article, news
from .filters import PostFilter
from .forms import PostForm, PostDeleteForm


# Create your views here.
# Представление для просмотра всех публикаций
class NewsList(ListView):
    model = Post
    ordering = '-datetime_in'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


# Представление для просмотра отдельной публикации
class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


# Представление для поиска публикаций
class PostSearch(ListView):
    model = Post
    ordering = '-datetime_in'
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 10
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
    # модель товаров,
    model = Post
    # шаблон, в котором используется форма,
    template_name = 'news_create.html'
    # и требование права на добавление новости.
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_type = news
        post.author = Author.objects.get(user_id=self.request.user.id)
        return super().form_valid(form)


# Представление, изменяющее новость
class NewsEdit(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('news.change_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_type = news
        return super().form_valid(form)


# Представление, удаляющее новость
class NewsDelete(PermissionRequiredMixin, DeleteView):
    form_class = PostDeleteForm
    model = Post
    template_name = 'news_delete.html'
    permission_required = ('news.delete_post',)
    success_url = reverse_lazy('news_list')


# Представление, создающее статью
class ArticleCreate(PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму,
    form_class = PostForm
    # модель товаров,
    model = Post
    # шаблон, в котором используется форма,
    template_name = 'article_create.html'
    # и требование права на добавление статьи.
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_type = article
        post.author = Author.objects.get(user_id=self.request.user.id)
        return super().form_valid(form)


# Представление, изменяющее статью
class ArticleEdit(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'
    permission_required = ('news.change_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_type = article
        return super().form_valid(form)


# Представление, удаляющее статью
class ArticleDelete(PermissionRequiredMixin, DeleteView):
    form_class = PostDeleteForm
    model = Post
    template_name = 'article_delete.html'
    permission_required = ('news.delete_post',)
    success_url = reverse_lazy('news_list')


@login_required
def make_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        Author.objects.create(user=user)
        authors_group.user_set.add(user)
    return redirect('/news/')
