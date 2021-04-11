from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import CustomUser, Post
from .serializers import CustomUserSerializer, PostSerializer


# Criar api dados usuário
class CustomUserViewSet(viewsets.ModelViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        user = self.get_object()
        serializer = PostSerializer(user.posts.all(), many=True)
        return Response(serializer.data)


# Criar api dados post
class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer