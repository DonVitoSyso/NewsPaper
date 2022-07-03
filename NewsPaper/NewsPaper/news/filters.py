# D4
from django_filters import (FilterSet, CharFilter, ModelChoiceFilter,
                            DateFilter,
                            ) # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post, Author, Category
from django import forms


# создаём фильтр
class PostFilter(FilterSet):
    date = DateFilter(
        label='Дата',
        lookup_expr='lte',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control pure-input-1-2'}),
    )
    # мы хотим чтобы нам выводило имя хотя бы отдалённо похожее на то что запросил пользователь
    title = CharFilter(
        lookup_expr='icontains',
        label='Название статьи',
        # D6 для оформеления поиска
        widget=forms.TextInput(attrs={'class': 'form-control pure-input-1-2', 'placeholder': 'Post Title'}),
    )
    # мы хотим чтобы нам выводило имя из списка
    author = ModelChoiceFilter(
        queryset=Author.objects.all(),
        label='Автор',
        empty_label='Все авторы',
        # D6
        widget=forms.Select(attrs={'class': 'form-control pure-input-1-2'}),
    )
    # мы хотим чтобы нам выводило категория списком
    category = ModelChoiceFilter(
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Все категории',
        # D6
        widget=forms.Select(attrs={'class': 'form-control pure-input-1-2'}),
    )
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться
    # (т. е. подбираться) информация о товарах
    class Meta:
        model = Post
        fields = ['date', 'title', 'author', 'category']
