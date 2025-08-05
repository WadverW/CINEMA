from django.urls import path
from . import views

app_name = "cinema"

urlpatterns = [
    path("", views.home, name="home"),
    path("afisha/", views.afisha, name="afisha"),
    path("movie/", views.movie_detail, name="movie_detail"),
    path("soon/", views.soon, name="soon"),
    path("promos/", views.promos, name="promos"),
    path("schedule/", views.schedule, name="schedule"),
    path("about", views.about_cinema, name="about_cinema"),
    path("cinemas/", views.cinemas, name="cinemas"),
    #
    path("cinema/", views.cinema_detail, name="cinema"),
    path("hall/", views.hall_detail, name="hall_detail"),
    # =============================== about cinemas links
    path("news/", views.news, name="news"),
    path("advertise/", views.advertise, name="advertise"),
    path("cafe/", views.cafe, name="cafe"),
    path("mobile-apps/", views.mobile_apps, name="mobile_apps"),
    path("contacts/", views.contacts, name="contacts"),
]
