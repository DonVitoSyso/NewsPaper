from django.shortcuts import render
# D3
# импортируем класс получения деталей объекта
from django.views.generic import ListView , DetailView
# импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from .models import Post
# from django.views import View


# D3
class NewsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # шаблон, в котором будет лежать HTML, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news' # список объектов данной модели из БД, для дальнейшей работы с ним в html-шаблоне
    # queryset = Post.objects.order_by('-dateCreated')
    ordering = ['-date']


# D3
class PostView(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


# D3
# class HomePageView(View):
#     template_name = "index.html"