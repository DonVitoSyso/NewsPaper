from django.urls import path #D3
from .views import (NewsList, PostView, # D3
                    PostSearch, # D4
                    )


#D3
urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно, почему
    path('', NewsList.as_view()),  # т. к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('<int:pk>', PostView.as_view(), name='new'),
    # D4
    path('search/', PostSearch.as_view(), name='search'),
    path('search/<int:pk>', PostView.as_view(), name='new_search'),
]