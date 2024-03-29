from django.urls import path #D3
from .views import (NewsList, PostView, # D3
                    PostSearch, PostCreateView, PostUpdateView, PostDeleteView, ArticleCreateView, # D4
                    PostCategory, subscribe_to_category, unsubscribe_from_category, ProfileView # D6
                    )
# D8_3
from django.views.decorators.cache import cache_page

# D3
urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно, почему
    # D5_4 - add news_list
    # представление NewList запускается с гланой страницы
    # path('', cache_page(60 * 1)(NewsList.as_view()), name='news_list'),
    # т. к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    # D8_3 начало
    path('', cache_page(60*1)(NewsList.as_view()), name='news_list'),  # кэширование гл страницы 1 мин
    # path('<int:pk>', cache_page(60*5)(PostView.as_view()), name='new'), # кэширование страницы с новостями 5 мин
    path('<int:pk>', PostView.as_view(), name='new'),
    # D8_3 конец
    # D4
    path('search/', PostSearch.as_view(), name='search'),
    path('search/<int:pk>', PostView.as_view(), name='new_search'),
    path('new/create/', PostCreateView.as_view(), name='new_create'),
    path('new/<int:pk>/edit', PostUpdateView.as_view(), name='new_update'),
    path('new/<int:pk>/delete', PostDeleteView.as_view(), name='new_delete'),
    path('article/create/', ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/edit', PostUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete', PostDeleteView.as_view(), name='article_delete'),
    # D6
    path('category/<int:pk>', PostCategory.as_view(), name='post_category'),
    path('subscribe/<int:pk>', subscribe_to_category, name='subscr_category'),
    path('unsubscribe/<int:pk>', unsubscribe_from_category, name='unsubscr_category'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
