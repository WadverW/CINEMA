from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    # Баннеры
    path("banners/", views.banners, name="banners"),
    path("contact-page/", views.contact_page, name="contact_page"),
    # Фильмы
    path("movies/", views.movies_list, name="movies_list"),
    path("movies/create/", views.movie_create, name="movie_create"),
    # Кинотеатры
    path("cinemas/", views.cinemas_list, name="cinemas_list"),
    path("cinemas/create/", views.cinema_create, name="cinema_create"),
    path("cinemas/<slug:slug>/", views.cinema_edit, name="cinema_edit"),
    path("cinemas/<slug:slug>/delete/", views.cinema_delete, name="cinema_delete"),
    path("cinemas/<slug:cinema_slug>/halls/", views.halls_table, name="halls_table"),
    path("cinemas/<slug:cinema_slug>/halls/create/", views.hall_create, name="hall_create"),  
    path("cinemas/<slug:cinema_slug>/halls/<int:pk>/", views.hall_edit, name="hall_edit"),
    path("cinemas/<slug:cinema_slug>/halls/<int:pk>/delete/", views.hall_delete, name="hall_delete"),   
    # Главная
    path("main-page/", views.main_page, name="main_page"),
    # Страницы
    path("page/<slug:slug>/", views.page_edit, name="page_edit"),
]
