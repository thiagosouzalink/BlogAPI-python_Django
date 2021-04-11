from django.urls import path

from rest_framework.routers import SimpleRouter

from . import views
from .api.api_views import CustomUserViewSet, PostViewSet


# Rotas geredas para api
router = SimpleRouter()
router.register('users', CustomUserViewSet)
router.register('posts', PostViewSet)

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('user/cadastro/', views.UserCadastroCreateView.as_view(), name='user_new'),
    path('user/edit/<str:username>/<int:user_id>/', views.UserEditUpdateView.as_view(), name='user_edit'),
    
    path('post/new/', views.PostCreateView.as_view(), name='post_new'),
    path('post/<str:username>/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<str:username>/update/<int:post_id>/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<str:username>/delete/<int:post_id>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('user/<str:username>/', views.user_perfil, name='user_perfil'),
]   