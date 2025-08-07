from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENDER_CHOICES = [("male", "Мужской"), ("female", "Женский")]
    LANGUAGE_CHOICES = [("ru", "Русский"), ("uk", "Українська")]

    phone_number = models.CharField(max_length=20)
    birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    card_number = models.CharField(max_length=20)
    nickname = models.CharField(max_length=100)

    def __str__(self):
        return self.nickname or self.username
