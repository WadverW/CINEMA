from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path("movies/", views.movie_list, name="movies"),
    path("cinemas/", views.cinema_list, name="cinemas"),
    path("halls/", views.hall_list, name="halls"),
    path("schedule/", views.schedule_list, name="schedule"),
    path("promotions/", views.promotion_list, name="promotions"),
    path("galleries/", views.gallery_list, name="galleries"),
    path("bookings/", views.booking_list, name="bookings"),
    path("users/", views.user_list, name="users"),
    path("seo/", views.seo_list, name="seo"),
    path("pages/", views.page_list, name="pages"),
]
