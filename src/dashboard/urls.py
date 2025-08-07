from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    # Главная
    path("", views.index, name="index"),
    # path("stats/", views.stats, name="stats"),
    # Баннеры
    path("banners/", views.banners, name="banners"),
    # Фильмы
    path("movies_admin/", views.movies_admin, name="movies_admin"),
    path("movies_admin/create/", views.movies_create, name="movies_create"),
    # path("movies/<int:pk>/", views.movie_edit, name="movie_edit"),
    # Кинотеатры
    path("cinemas_admin/", views.cinema_list, name="cinemas_admin"),
    path("cinemas_admin/create/", views.cinema_create, name="cinemas_create"),
    path("cinemas/hall/create/", views.hall_create, name="hall_create"),
    # Новости и Акции
    path("news_admin/", views.news_list, name="news"),
    path("news_admin/create/", views.news_create, name="news_create"),
    path("promotions/", views.promotions, name="promotions"),
    # Страницы
    path("pages/main/", views.page_main, name="main_page"),
    path("pages/about/", views.page_about, name="about"),
    path("pages/cafe/", views.page_cafe, name="cafe"),
    path("pages/vip/", views.page_vip, name="vip"),
    path("pages/kids/", views.page_kids, name="kids"),
    path("pages/ads/", views.page_ads, name="ads"),
    path("pages/contacts/", views.page_contacts, name="contacts"),
    #
    path("users/", views.users, name="users"),
    #
    path("mailing/", views.mailing, name="mailing"),
]
