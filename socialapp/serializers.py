from rest_framework import serializers
from .models import Tag, Post, Like

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class PostListSerializer(serializers.ModelSerializer):
    liked = serializers.SerializerMethodField()
    disliked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'images', 'description', 'liked', 'disliked', 'likes', 'dislikes', 'created_date']

    def get_liked(self, obj):
        user = self.context.get('user')
        if user:
            try:
                like = Like.objects.get(user=user, post=obj)
                return like.liked
            except Like.DoesNotExist:
                pass
        return False

    def get_disliked(self, obj):
        user = self.context.get('user')
        if user:
            try:
                like = Like.objects.get(user=user, post=obj)
                return like.disliked
            except Like.DoesNotExist:
                pass
        return False
