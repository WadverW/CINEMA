from django.db import models
from users.models import User
from cinema.models import Movie, Hall


class Screening(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    language = models.CharField(max_length=50)
    format = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.movie.title} в {self.hall.name} ({self.start_time})"


class Ticket(models.Model):
    STATUS_CHOICES = [("reserved", "Забронирован"), ("paid", "Оплачен")]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    seat_row = models.IntegerField()
    seat_number = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
