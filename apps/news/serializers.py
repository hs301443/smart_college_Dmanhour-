from datetime import datetime
from rest_framework import serializers
from .models import NewImage, NewVideo, NewsPdf, NewsArticle

class NewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewImage
        fields = ['id', 'image', 'news_article']


class NewVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewVideo
        fields = ['id', 'video', 'news_article']


class NewsPdfSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsPdf
        fields = ['id', 'pdf', 'news_article']




class NewsArticleSerializer(serializers.ModelSerializer):
    images = NewImageSerializer(many=True, read_only=True)
    videos = NewVideoSerializer(many=True, read_only=True)
    pdfs = NewsPdfSerializer(many=True, read_only=True)

    class Meta:
        model = NewsArticle
        fields = [
            'id', 'title', 'description',
            'content', 'keywords', 
            'source', 'image', 'created_at', 'updated_at',
            'ar_new_type', 'is_active', 'is_event',
            'month', 'event_date', 'event_link', 'images', 'videos', 'pdfs',
        ]
        read_only_fields = ['created_at', 'updated_at']


