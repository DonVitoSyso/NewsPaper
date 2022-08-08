# D5
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from news.models import Author
# D5_5
from django.shortcuts import render


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'
    template_name = '/signup.html'

    # D5_5 для добавления пользователя в группу по умолчанию
    def post(self, request, *args, **kwargs):
        form = BaseRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            user_group = Group.objects.get(name='common')
            user.groups.add(user_group)
            return redirect('login')
        else:
            return render(request, self.template_name, {'form': form})


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')

    if not request.user.groups.filter(name='authors').exists():
        # мой код
        # user1 = Author(user=user) сохраняем нашего пользователя в список авторов модели
        # user1.save()
        # код из FAQ
        Author.objects.create(username=user)
        author_group.user_set.add(user)
    else:
        Author.objects.filter(username=user).delete()
        author_group.user_set.remove(user)
    return redirect('/')
