# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post
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


# Представление для просмотра отдельной публикации
class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


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
        return context


# Представление, создающее новость
class NewsCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_type = news
        return super().form_valid(form)


# Представление, изменяющее новость
class NewsEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_type = news
        return super().form_valid(form)


# Представление, удаляющее новость
class NewsDelete(DeleteView):
    form_class = PostDeleteForm
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_type = news
        return super().form_valid(form)


# Представление, создающее статью
class ArticleCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'article_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_type = article
        return super().form_valid(form)


# Представление, изменяющее статью
class ArticleEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_type = article
        return super().form_valid(form)


# Представление, удаляющее статью
class ArticleDelete(DeleteView):
    form_class = PostDeleteForm
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_type = article
        return super().form_valid(form)
