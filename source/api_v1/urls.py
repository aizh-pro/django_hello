from django.urls import path

from api_v1.views import get_token_view, ArticleListView, ArticleCreateView, ArticleDetailView, ArticleUpdateView, \
    ArticleFullView, ArticleDeleteView

app_name = 'api_v1'

urlpatterns = [
    path('get-token/', get_token_view, name='get_token'),
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('article/create/', ArticleCreateView.as_view(), name='article_create'),
    path('article/detail/<int:pk>/', ArticleDetailView.as_view(), name='article_view'),
    path('article/update/<int:pk>/', ArticleUpdateView.as_view(), name='article_update_view'),
    path('article/delete/<int:pk>/', ArticleDeleteView.as_view(), name='article_delete_view'),
    path('article/<int:pk>/', ArticleFullView.as_view(), name='article_full_view'), # здесь в одном view можно удалить, просмотреть, изменить статью
]