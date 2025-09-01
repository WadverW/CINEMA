from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class SeoBlock(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    keywords = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Image(models.Model):
    image = models.ImageField(upload_to="gallery/", null=True, blank=True)
    alt_text = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Cinema(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True)
    city = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    description = models.TextField()
    map_coordinates = models.CharField(max_length=100)
    image = models.ImageField(upload_to="cinema/", null=True, blank=True)
    gallery = models.ManyToManyField(Image, related_name="cinemas", blank=True)
    seo = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Hall(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name="halls")
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    description = models.TextField(blank=True)
    is_vip = models.BooleanField(default=False)
    seo = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True, blank=True)
    map_hall = models.ImageField(upload_to="hall_maps/", null=True, blank=True)
    gallery = models.ManyToManyField(Image, related_name="halls", blank=True)

    def __str__(self):
        return f"{self.name} ({self.cinema.name})"


class Movie(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    poster = models.ImageField(upload_to="posters/", null=True, blank=True)
    trailer_url = models.URLField()
    age_rating = models.CharField(max_length=10)
    release_date = models.DateField()
    is_coming_soon = models.BooleanField(default=False)
    gallery = models.ManyToManyField(Image, related_name="movies", blank=True)
    is_2d = models.BooleanField(default=True)
    is_3d = models.BooleanField(default=False)
    is_imax = models.BooleanField(default=False)
    seo = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
            if not self.slug:
                self.slug = slugify(self.title)
            super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("cinema:movie_detail", kwargs={"slug": self.slug})
