from rest_framework import serializers

from django.contrib.auth.models import User

from .models import Post, Category, Author


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), write_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, write_only=True)
    post_rating = serializers.StringRelatedField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'url',
            'id',
            'news_type',
            'datetime_in',
            'headline',
            'content',
            'post_rating',
            'author',
            'category',
            'author_id',
            'category_id'
        ]


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    subscribers = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'url',
            'id',
            'name',
            'subscribers'
        ]


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    author_rating = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Author
        fields = [
            'url',
            'id',
            'author_rating',
            'user'
        ]
