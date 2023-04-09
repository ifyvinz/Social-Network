from .models import User, Post, Profile
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    likes =  serializers.StringRelatedField(many=True)
    timestamp = serializers.DateTimeField(format="%I:%M %p, %a %d %B %Y")
    class Meta:
        model = Post
        fields = ['id', 'author', 'body', 'timestamp', 'likes']

class ProfileSerializer(serializers.ModelSerializer):
    user =serializers.StringRelatedField()
    name = serializers.StringRelatedField()
    about =serializers.StringRelatedField()
    country = serializers.StringRelatedField()
    photo = serializers.ImageField()
    class Meta:
        model = Profile
        fields = ['id', 'user', 'name', 'about', 'country', 'photo']