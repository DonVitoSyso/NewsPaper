from django.contrib import admin
from .models import Author, Post, Category, CatSub


admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(CatSub)