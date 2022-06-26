from django.shortcuts import render
# D3
# импортируем класс получения деталей объекта
from django.views.generic import (
                                    ListView, DetailView,
                                    CreateView, UpdateView, DeleteView, # D4
                                  )
# импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from .models import (
                        Post,
                        Category, # D4
                     )
# from django.views import View
# D4
from .filters import PostFilter
from .forms import (
                    PostForm,
                    AuthorForm, #D5
                    )
# D5
from django.contrib.auth.mixins import LoginRequiredMixin


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

    # D5
    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон.
    # В возвращаемом словаре context будут храниться все переменные. Ключи этого словаря и есть переменные,
    # к которым мы сможем потом обратиться через шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=super().get_queryset())  # вписываем наш фильтр в контекст
        # context['form'] = PostForm
        return context


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
    # D4
    paginate_by = 10

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=super().get_queryset())  # вписываем наш фильтр в контекст
        context['categories'] = Category.objects.all()
        context['form'] = PostForm
        return context

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        queryset = super().get_queryset()
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


# D4. Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
# D5 LoginRequiredMixin в параметрах
class PostCreateView(LoginRequiredMixin, CreateView):
    # Проверка на права доступа
    template_name = 'new_create.html' # имя шаблона
    form_class = PostForm # класс формы
    model = Post # класс для работы с валидацией ниже

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NEWS'
        validated = super().form_valid(form)

        return validated


# D5 LoginRequiredMixin в параметрах
class PostUpdateView(LoginRequiredMixin, UpdateView):
    # Проверка на права доступа
    template_name = 'new_create.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        post = Post.objects.get(pk=id)
        post.isUpdated = True
        return post


# D5 LoginRequiredMixin в параметрах
class PostDeleteView(LoginRequiredMixin, DeleteView):
    # Проверка на права доступа
    success_url = '/news/'
    template_name = 'new_delete.html'

    # ИЗ ЭТАЛОНА
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# D5 LoginRequiredMixin в параметрах
class ArticleCreateView(LoginRequiredMixin, CreateView):
    # Проверка на права доступа
    template_name = 'new_create.html'
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'ARTICLE'
        validated = super().form_valid(form)

        return validated


# D5
class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'author_update.html'
    form_class = AuthorForm

    def get_object(self, **kwargs):
        return self.request.user
