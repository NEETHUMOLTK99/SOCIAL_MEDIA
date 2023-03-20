from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Tag, Post, Like
from .serializers import TagSerializer, PostSerializer, LikeSerializer, PostListSerializer

class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAdminUser]

class PostList(generics.ListCreateAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            likes = Like.objects.filter(user=user)
            liked_posts = [like.post.id for like in likes if like.liked]
            disliked_posts = [like.post.id for like in likes if like.disliked]
            posts = Post.objects.exclude(id__in=liked_posts+disliked_posts)
            if liked_posts:
                liked_posts_qs = Post.objects.filter(id__in=liked_posts)
                posts = posts | liked_posts_qs
            if disliked_posts:
                disliked_posts_qs = Post.objects.filter(id__in=disliked_posts)
                posts = posts | disliked_posts_qs
        else:
            posts = Post.objects.all()
        return posts.order_by('-created_date')

    def create(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class LikeCreate(generics.CreateAPIView):
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LikeList(generics.ListAPIView):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    permission_classes = [permissions.IsAdminUser]

