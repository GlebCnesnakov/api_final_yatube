# TODO:  Напишите свой вариант
from posts.models import Post, Comment, Group, Follow
from .serializers import PostSerializer, CommentSerializer
from .serializers import GroupSerializer, FollowSerializer
from rest_framework import viewsets, filters, mixins
from .permissions import OwnerOrReadOnly, ReadOnly
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly,)

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=Post.objects.get(id=self.kwargs['post_id'])
        )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (ReadOnly,)


class FollowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def create(self, request):
        serializer = FollowSerializer(data=request.data)
        v = serializer.is_valid()
        c = self.request.user.username  # pep8 ругается
        if v and serializer.validated_data['following'].username != c:
            x = serializer.validated_data['following']
            if Follow.objects.filter(
                user=self.request.user,
                following=x
            ).exists():
                return Response(
                    {"error": "Подписка уже существует"},
                    status=400
                )
            serializer.save(
                following=x,
                user=self.request.user
            )
            return Response(serializer.data, status=201)
        return Response(
            {"error": "Нельзя подписаться на самого себя."}, status=400)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
