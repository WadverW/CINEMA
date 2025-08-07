from django.db import models


class SeoBlock(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    keywords = models.CharField(max_length=200)
    slug = models.SlugField()

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to="gallery/")
    alt_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class Cinema(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    city = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    description = models.TextField()
    map_coordinates = models.CharField(max_length=100)
    image = models.ImageField(upload_to="cinema/")
    seo = models.OneToOneField(SeoBlock, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Hall(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    is_vip = models.BooleanField(default=False)
    seo = models.OneToOneField(SeoBlock, on_delete=models.CASCADE)
    map_hall = models.ImageField(upload_to="hall_maps/")

    def __str__(self):
        return f"{self.name} ({self.cinema.name})"


class Movie(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField()
    poster = models.ImageField(upload_to="posters/")
    trailer_url = models.URLField()
    age_rating = models.CharField(max_length=10)
    release_date = models.DateField()
    is_coming_soon = models.BooleanField(default=False)
    gallery = models.ManyToManyField(Image)
    is_2d = models.BooleanField(default=True)
    is_3d = models.BooleanField(default=False)
    is_imax = models.BooleanField(default=False)
    seo = models.OneToOneField(SeoBlock, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
