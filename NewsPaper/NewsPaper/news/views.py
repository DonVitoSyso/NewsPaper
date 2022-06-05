from django.shortcuts import render
# D3
# импортируем класс получения деталей объекта
from django.views.generic import ListView , DetailView
# импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from .models import (Post,
                     Category, # D4
                     )
# from django.views import View
# D4
from .filters import PostFilter
from .forms import PostForm


# D3
class NewsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # шаблон, в котором будет лежать HTML, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news' # список объектов данной модели из БД, для дальнейшей работы с ним в html-шаблоне
    # queryset = Post.objects.order_by('-dateCreated')
    ordering = ['-date']
    # D4
    paginate_by = 10  # постраничный вывод
    form_class = PostForm  # добавляем форм класс, чтобы получать доступ к форме через метод POST


# D3
class PostView(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


# D3
# class HomePageView(View):
#     template_name = "index.html"


# D4
class PostSearch(ListView):
    template_name = 'search.html'
    context_object_name = 'posts'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        context['categories'] = Category.objects.all()
        context['form'] = PostForm

        return context