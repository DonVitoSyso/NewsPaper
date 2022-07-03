# D4
from django.forms import ModelForm, CharField, ModelChoiceField
from .models import Post, Category, User, Author
from django.core.exceptions import ValidationError
from django import forms


# Создаём модельную форму для создания статьи
class PostForm(ModelForm):
    # тоже самое, что и метод clean
    # text = forms.CharField(min_length=20)

    # мы хотим чтобы нам выводило категория списком
    # category = ModelChoiceField(
    #     queryset=Category.objects.all(),
    #     empty_label=None,
    # )
    # в класс мета, как обычно, надо написать модель, по которой будет строится форма и нужные нам поля.
    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'category']
        widgets = {
            'author': forms.Select(attrs={'class': 'form-control pure-input-1-2'}),
            'category': forms.SelectMultiple(attrs={'class': 'form-control pure-input-1-2'}),
            'title': forms.TextInput(attrs={'class': 'form-control pure-input-1-2', 'placeholder': 'Post Title'}),
            'text': forms.Textarea(attrs={'class': 'form-control pure-input-1-2'}),
        }

    # создание своего метода проверки
    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text is not None and len(text) < 20:
            raise ValidationError({
                "text": "Статья не может быть менее 20 символов."
            })

        return cleaned_data


# D5
# Создаём модельную форму Для Авторов
class AuthorForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
