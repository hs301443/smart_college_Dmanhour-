from cloudinary_storage.storage import MediaCloudinaryStorage
from django.db import models
from apps.units.models import unit
from cloudinary.models import CloudinaryField
class NewImage(models.Model):
    image = models.ImageField(upload_to='damanhour/news/images/', storage=MediaCloudinaryStorage())
    news_article = models.ForeignKey('NewsArticle', related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.news_article.title}"
    
class NewVideo(models.Model):
    video = CloudinaryField(
        resource_type='video',
        folder='damanhour/news/videos/',
        blank=True, null=True
    )
    news_article = models.ForeignKey('NewsArticle', related_name='videos', on_delete=models.CASCADE)

    def __str__(self):
        return f"Video for {self.news_article.title}"
    
class NewsPdf(models.Model):
    pdf = models.FileField(upload_to='damanhour/news/pdfs/', storage=MediaCloudinaryStorage())
    news_article = models.ForeignKey('NewsArticle', related_name='pdfs', on_delete=models.CASCADE)

    def __str__(self):
        return f"PDF for {self.news_article.title}"

class NewsArticle(models.Model):
    AR_NEWS_TYPES = [
        ('اعلان', 'اعلان'),
        ('حدث', 'حدث'),
        ('خبر', 'خبر'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    content = models.TextField()
    keywords = models.JSONField(blank=True, null=True, default=list)
    source = models.CharField(max_length=255, blank=True, null=True)

    image = models.ImageField(upload_to='damanhour/news/main_images/', storage=MediaCloudinaryStorage(), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ar_new_type = models.CharField(max_length=20, choices=AR_NEWS_TYPES)
    is_active = models.BooleanField(default=True)
    is_event = models.BooleanField(default=False)
    month = models.PositiveIntegerField(blank=True, null=True)
    event_date = models.DateField(blank=True, null=True)
    event_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.get_ar_new_type_display()})"
