from django.db import models
# D2
from django.contrib.auth.models import User
from django.db.models import Sum


# D2
class Author(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    # Делаем нормальный вывод имени пользователя
    def __str__(self):
        return f'{self.username}'

    def update_rating(self):
        # Суммарный рейтинг каждой статьи автора умножается на 3
        postR = self.post_set.aggregate(postRating=Sum('rating'))
        pR = 0
        # Проверка на присутвие данный в запросе postR
        if postR.get('postRating') is not None:
            pR += postR.get('postRating')

        # Суммарный рейтинг всех комментариев автора
        comR = self.username.comment_set.aggregate(commentRating=Sum('rating'))
        cR = 0
        if comR.get('commentRating') is not None:
            cR += comR.get('commentRating')

        # Суммарный рейтинг всех комментариев к статьям автора
        cpR = 0
        for pst in self.post_set.all():
            compostR = pst.comment_set.aggregate(commentpostRating=Sum('rating'))
            if compostR.get('commentpostRating') is not None:
                cpR += compostR.get('commentpostRating')

        self.rating = pR * 3 + cR + cpR
        self.save()


# Класс написан
class Category(models.Model):
    # D2
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}'


# Готов класс D2
class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    CAT_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    type = models.CharField(max_length=2, choices=CAT_CHOICES, default=ARTICLE)
    date = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    text = models.TextField(default='')
    title = models.CharField(max_length=255)
    rating = models.SmallIntegerField(default=0)

    # из эталона
    # isUpdated = models.BooleanField(default=False)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:123]}...'

    # из эталона
    def email_preview(self):
        return f'{self.text[0:50]}...'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с новостью
        return f'/news/{self.id}'

    # из эталона
    def get_cat(self):
        return self.type

    def __str__(self):
        return f'{self.date.date()} :: {self.author} :: {self.title} {self.type}'


# Класс написан D2
class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)
    # из эталона
    # def __str__(self):
    #     return f'{self.category} -> {self.post}'


# Класс написан D2
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    # из эталона
    def __str__(self):
        try:
            return self.post.author.user
        except:
            return self.user.username
