from rest_framework import viewsets
from rest_framework import permissions

from .permissions import IsOwnerOrReadOnly
from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrReadOnly]

    def get_queryset(self):
        post = Post.objects.get(id=self.kwargs.get("post_id"))
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs.get("post_id"))
        serializer.save(author=self.request.user, post=post)
