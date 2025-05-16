from rest_framework import serializers
from .models import NewImage, NewVideo, NewsPdf, NewsArticle
from datetime import datetime

class NewImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = NewImage
        fields = ['id', 'image', 'news_article']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None


class NewVideoSerializer(serializers.ModelSerializer):
    video = serializers.SerializerMethodField()

    class Meta:
        model = NewVideo
        fields = ['id', 'video', 'news_article']

    def get_video(self, obj):
        request = self.context.get('request')
        if obj.video and hasattr(obj.video, 'url'):
            return request.build_absolute_uri(obj.video.url) if request else obj.video.url
        return None


class NewsPdfSerializer(serializers.ModelSerializer):
    pdf = serializers.SerializerMethodField()

    class Meta:
        model = NewsPdf
        fields = ['id', 'pdf', 'news_article']

    def get_pdf(self, obj):
        request = self.context.get('request')
        if obj.pdf and hasattr(obj.pdf, 'url'):
            return request.build_absolute_uri(obj.pdf.url) if request else obj.pdf.url
        return None


class NewsArticleSerializer(serializers.ModelSerializer):
    images = NewImageSerializer(many=True, read_only=True)
    videos = NewVideoSerializer(many=True, read_only=True)
    pdfs = NewsPdfSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

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

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Arabic title is required.")
        return value

    def validate_event_date(self, value):
        if value and value < datetime.now().date():
            raise serializers.ValidationError("Event date must be a future date.")
        return value

    def validate(self, data):
        if data.get('event_date') and data['event_date'] < data.get('created_at', datetime.now().date()):
            raise serializers.ValidationError("Event date cannot be earlier than the creation date.")
        return data
