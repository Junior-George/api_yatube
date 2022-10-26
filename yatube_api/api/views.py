from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsOwnerOrReadOnly
from rest_framework import permissions

from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_retriev(self, serializer, pk):
        posts = Post.objects.all()
        post = get_object_or_404(posts, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def perform_list(self, serializer):
        posts = Post.objects.all()
        serializer = PostSerializer(posts)
        return Response(serializer.data)

    def part_update(self, request, pk):
        posts = Post.objects.all()
        post = get_object_or_404(posts, pk=pk)
        serializer = PostSerializer(posts, post)
        if serializer.is_valid() and request.user == post.author:
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        post = Post.objects.get(pk=pk)
        user = request.user
        if user == post.author:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


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

    def part_update(self, request, pk):
        comments = Comment.objects.all()
        comment = get_object_or_404(comments, pk=pk)
        serializer = PostSerializer(comments, comment)
        if serializer.is_valid() and request.user == comment.author:
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        user = request.user
        if user == comment.author:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)
