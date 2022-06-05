# D4
from django.forms import ModelForm, CharField, ModelChoiceField
from .models import Post, Category, User, Author
from django.core.exceptions import ValidationError
from django import forms


# Создаём модельную форму
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

    # создание своего метода проверки
    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text is not None and len(text) < 20:
            raise ValidationError({
                "text": "Статья не может быть менее 20 символов."
            })

        return cleaned_data
