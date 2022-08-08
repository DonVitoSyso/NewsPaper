from django.contrib import admin
from .models import Author, Post, Category, CatSub, PostCategory, Comment


admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(CatSub)
admin.site.register(PostCategory)
admin.site.register(Comment)
