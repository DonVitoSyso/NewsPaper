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
                        CatSub, # D6
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
# D6
from django.shortcuts import redirect
from django.urls import resolve
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from django.core.mail import EmailMultiAlternatives  # импортируем класс для создание объекта письма с html
# D8_4
from django.core.cache import cache # импортируем наш кэш
#D6 удалить после настройкки signals
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import mail_managers
# from django.dispatch import receiver # импортируем нужный декоратор

#D6 удалить после настройкки signals
# создаём функцию обработчик с параметрами под регистрацию сигнала
# @receiver(post_save, sender=Post)
# def notify_managers_appointment(sender, instance, created, **kwargs):
#     subject = f'{instance.title} {instance.date.strftime("%d %m %Y")}'
#
#     # mail_managers(
#     #     subject=subject,
#     #     message=instance.text,
#     # )
#     msg = EmailMultiAlternatives(
#         subject=subject, #kwargs['email_subject'],
#         from_email='vitosyso@yandex.ru',
#         to=['vitosyso@yandex.ru',] #kwargs['user_emails']  # отправляем всем из списка
#     )
#     # msg.attach_alternative(html, 'text/html')
#     msg.send()
#     print("Signal_old_type....")


# коннектим наш сигнал к функции обработчику и указываем, к какой именно модели после сохранения привязать функцию
# post_save.connect(notify_managers_appointment, sender=Post)


# D3
class NewsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # шаблон, в котором будет лежать HTML, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news' # список объектов данной модели из БД, для дальнейшей работы с ним в html-шаблоне
    # queryset = Post.objects.order_by('-dateCreated')
    ordering = ['-date']
    # D4
    paginate_by = 9  # постраничный вывод
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
    # D8_4
    queryset = Post.objects.all()

    # D8_4
    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        # кэш очень похож на словарь, и метод get действует так же.
        # Он забирает значение по ключу, если его нет, то забирает None.
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


# D3
# class HomePageView(View):
#     template_name = "index.html"


# D4
class PostSearch(ListView):
    template_name = 'search.html'
    context_object_name = 'posts'
    queryset = Post.objects.all()
    # D4
    paginate_by = 6
    ordering = ['-date']

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
    # model = Post # класс для работы с валидацией ниже

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NW'
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
        post.type = 'AR'
        validated = super().form_valid(form)

        return validated


# D5
class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'author_update.html'
    form_class = AuthorForm

    def get_object(self, **kwargs):
        return self.request.user


# D6 весь код ниже для подписки
class PostCategory(ListView):
    model = Post
    # не работает почему-то
    ordering = ['-date']
    template_name = 'subcat/filtered.html'
    context_object_name = 'news'
    paginate_by = 6


    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        queryset = Post.objects.filter(category=Category.objects.get(id=self.id))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())
        context['name'] = Category.objects.get(id=self.id)
        return context


# Подписка пользователя в категорию новостей
@login_required
def subscribe_to_category(request, pk):
    user = request.user
    cat = Category.objects.get(id=pk)

    if not cat.subscribers.filter(id=user.id).exists():
        cat.subscribers.add(user)
        # получаем наш созданный html
        html = render_to_string(
            'subcat/subscribed.html',
            {'categories': cat, 'user': user},
            # передаем в шаблон какие захотим переменные, в данном случае я просто передал категорию для вывода ее в письме
        )
        msg = EmailMultiAlternatives(
            subject=f'На {cat} категорию подписаны',
            from_email='vitosyso@yandex.ru',
            to=[user.email, ],
        )

        msg.attach_alternative(html, 'text/html') # добавляем html
        try:
            msg.send() # отсылаем
        except Exception as e:
            print(e)
        return redirect('profile')

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe_from_category(request, pk):
    user = request.user
    cat = Category.objects.get(id=pk)

    if cat.subscribers.filter(id=user.id).exists():
        cat.subscribers.remove(user)
    return redirect('profile')


class ProfileView(ListView):
    model = CatSub
    template_name = 'profile.html'
    context_object_name = 'categories'
# D6 - код для подписки закончен
