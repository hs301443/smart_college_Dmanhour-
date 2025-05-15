from django.db import models
from apps.units.models import unit

class NewImage(models.Model):
    image = models.ImageField(upload_to='news/images/')
    news_article = models.ForeignKey('NewsArticle', related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.news_article.title}"
    
class NewVideo(models.Model):
    video = models.FileField(upload_to='news/videos/')
    news_article = models.ForeignKey('NewsArticle', related_name='videos', on_delete=models.CASCADE)

    def __str__(self):
        return f"Video for {self.news_article.title}"
    
class NewsPdf(models.Model):
    pdf = models.FileField(upload_to='news/pdfs/')
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

    image = models.ImageField(upload_to='news/', blank=True, null=True)
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


