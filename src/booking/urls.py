from django.urls import path
from . import views

app_name = "booking"
urlpatterns = [
    path("booking/", views.booking_view, name="booking"),
]
