from django.db import models
from cinema.models import SeoBlock, Image


class PromoNews(models.Model):
    TYPE_CHOICES = [("news", "Новость"), ("promo", "Акция")]

    title = models.CharField(max_length=255)
    slug = models.SlugField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    image = models.ImageField(upload_to="promo_news/", null=True, blank=True)
    gallery = models.ManyToManyField(Image, related_name="promo_news", blank=True)
    text = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    published_at = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    seo = models.OneToOneField(
        SeoBlock, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.title
