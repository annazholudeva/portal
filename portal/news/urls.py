from django.urls import path
from .views import (NewsList, NewsDetail, NewsCreate, NewsUpdate, NewsDelete,
                    NewsSearch, subscribe, CategoryList)

urlpatterns = [
   path('', NewsList.as_view(), name='allnews'),
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('search/', NewsSearch.as_view(), name='news_search'),
   path('<int:pk>', NewsDetail.as_view(), name='news'),
   path('<int:pk>/update/', NewsUpdate.as_view(), name='news_edit'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('categories/<int:pk>', CategoryList.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]
