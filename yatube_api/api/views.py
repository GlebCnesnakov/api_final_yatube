# TODO:  Напишите свой вариант
from posts.models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework import viewsets, permissions, filters
from .permissions import OwnerOrReadOnly, ReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (OwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def get_permissions(self):
    #     if self.action == 'retrieve':
    #         return (ReadOnly(),)
    #     return super().get_permissions()

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer