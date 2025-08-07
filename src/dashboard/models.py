from django.db import models
from cinema.models import SeoBlock, Cinema


class MainPage(models.Model):
    phone_1 = models.CharField(max_length=20)
    phone_2 = models.CharField(max_length=20)
    seo_text = models.TextField()
    is_active = models.BooleanField(default=True)
    language = models.CharField(
        max_length=2, choices=[("ru", "Русский"), ("uk", "Українська")]
    )
    seo = models.OneToOneField(SeoBlock, on_delete=models.CASCADE)


class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    content = models.TextField()
    image = models.ImageField(upload_to="static_pages/")
    seo = models.OneToOneField(SeoBlock, on_delete=models.CASCADE)


class ContactPage(models.Model):
    is_active = models.BooleanField(default=True)
    language = models.CharField(
        max_length=2, choices=[("ru", "Русский"), ("uk", "Українська")]
    )
    cinema = models.OneToOneField(Cinema, on_delete=models.CASCADE)
    seo = models.OneToOneField(SeoBlock, on_delete=models.CASCADE)


class BannerImage(models.Model):
    image = models.ImageField(upload_to="banners/")
    is_background = models.BooleanField(default=False)


class MainUpperBanner(models.Model):
    link = models.URLField()
    text = models.CharField(max_length=255)
    position = models.PositiveIntegerField()
    rotation_speed = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    image = models.ManyToManyField(BannerImage)


class BgBanner(models.Model):
    is_image_background = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to="background_banners/")


class NewsPromoBanner(models.Model):
    link = models.URLField()
    text = models.CharField(max_length=255)
    position = models.PositiveIntegerField()
    rotation_speed = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    image = models.ManyToManyField(BannerImage)
