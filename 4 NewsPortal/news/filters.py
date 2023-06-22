from django_filters import FilterSet, CharFilter, DateFilter
from .models import Post
from django.forms import DateInput

# Создаем свой набор фильтров для модели Post.
class PostFilter(FilterSet):
    # поиск по заголовку
    headline = CharFilter(label='Заголовок', lookup_expr='icontains')
    # по имени автора
    author__user__username = CharFilter(label='Имя автора', lookup_expr='iexact')
    # по дате публикации (после указываемой)
    datetime_in = DateFilter(widget=DateInput(attrs={'type': 'date'}), label='Время публикации (после)',
                             lookup_expr='date__gte')

    class Meta:
        # В Meta классе мы должны указать Django модель, в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели будет производиться фильтрация.
        fields = [
            'headline',
            'author__user__username',
            'datetime_in',
        ]
