from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, AccessMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


from .filters import ReplyFilter
from .forms import AdForm, ReplyDeleteForm, ReplyForm
from .models import Advertisement, Reply, Category


# Представление для просмотра всех объявлений
class AdsListView(ListView):
    model = Advertisement
    ordering = '-created_at'
    template_name = 'ads/ads_list.html'
    context_object_name = 'ads'
    paginate_by = 10


# Представление для просмотра конкретного объявления
def ad_detail_view(request, pk):
    template_name = 'ads/ad_detail.html'
    # получаем текущее объявление
    adv = get_object_or_404(Advertisement, id=pk)
    # список всех принятых откликов на это объявление
    replies = adv.replies.filter(approved=True)
    new_reply = None
    if request.method == 'POST':
        # Отклик оставлен
        reply_form = ReplyForm(data=request.POST)
        if reply_form.is_valid():
            # создаем объект отлика, но пока не сохраняем в БД
            new_reply = reply_form.save(commit=False)
            # привязываем отклик к текущему объявлению
            new_reply.adv = adv
            new_reply.user = request.user
            # сохраняем отклик в БД
            new_reply.save()
    else:
        reply_form = ReplyForm()

    context = {
        'adv': adv,
        'replies': replies,
        'new_reply': new_reply,
        'reply_form': reply_form
    }

    return render(request, template_name, context)


# Представление, создающее объявление
class AdCreateView(PermissionRequiredMixin, AccessMixin, CreateView):
    # Указываем нашу разработанную форму,
    form_class = AdForm
    # модель объявлений,
    model = Advertisement
    # шаблон, в котором используется форма,
    template_name = 'ads/ad_create.html'
    # и требование права на добавление объявления
    permission_required = ('ads.add_advertisement',)
    raise_exception = True

    def form_valid(self, form):
        author = User.objects.get(id=self.request.user.id)
        ad = form.save(commit=False)
        ad.author = author
        # вызываем метод super, чтобы у объявления появился pk
        result = super().form_valid(form)
        # ad_add_notification.delay(ad.pk)
        return result


# Представление, изменяющее объявление
class AdEditView(PermissionRequiredMixin, AccessMixin, UpdateView):
    form_class = AdForm
    model = Advertisement
    template_name = 'ads/ad_edit.html'
    # требование права на изменение объявления
    permission_required = ('ads.change_advertisement',)
    raise_exception = True


class AdsListByCategoryView(AdsListView):
    template_name = 'ads/category_list.html'
    context_object_name = 'category_ads_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Advertisement.objects.filter(category=self.category).order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


# Представление для подписки на выбранную категорию
@permission_required('ads.edit_category', raise_exception=True)
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    is_not_author = not request.user.groups.filter(name='authors').exists()
    data = {'category': category, 'is_not_author': is_not_author}
    return render(request, 'ads/subscribe.html', context=data)


# Представление для просмотра откликов с фильтрацией
class RepliesListView(PermissionRequiredMixin, AccessMixin, ListView):
    model = Reply
    ordering = '-created_at'
    template_name = 'reply/replies_list.html'
    context_object_name = 'replies'
    paginate_by = 10
    permission_required = ('ads.view_advertisement',)
    raise_exception = True

    # Переопределяем функцию получения списка откликов
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = ReplyFilter(self.request.GET, queryset.filter(adv__author=self.request.user), request=self.request)
        # Возвращаем из функции отфильтрованный список откликов
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset

        return context


# Представление, удаляющее отклик
class ReplyDeleteView(PermissionRequiredMixin, AccessMixin, DeleteView):
    form_class = ReplyDeleteForm
    model = Reply
    template_name = 'reply/reply_delete.html'
    # требование права на удаление отклика
    permission_required = ('ads.delete_reply',)
    raise_exception = True
    success_url = reverse_lazy('replies_list')


# Представление, принимающее отклик
@permission_required('ads.edit_reply', raise_exception=True)
def reply_approve_view(pk):
    # user = request.user
    reply = Reply.objects.get(id=pk)
    reply.approved = True
    reply.save()

    return redirect('/ads/replies/')


# Представление-заглушка для стартовой страницы
def startpage(request):
    return render(request, "index.html")
