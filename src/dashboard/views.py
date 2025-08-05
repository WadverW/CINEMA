from django.shortcuts import render


def home(request):
    return render(request, "dashboard/home.html")


def movie_list(request):
    return render(request, "dashboard/movies/list.html")


def cinema_list(request):
    return render(request, "dashboard/cinemas/list.html")


def hall_list(request):
    return render(request, "dashboard/halls/list.html")


def schedule_list(request):
    return render(request, "dashboard/schedule/list.html")


def promotion_list(request):
    return render(request, "dashboard/promotions/list.html")


def gallery_list(request):
    return render(request, "dashboard/galleries/list.html")


def booking_list(request):
    return render(request, "dashboard/bookings/list.html")


def user_list(request):
    return render(request, "dashboard/users/list.html")


def seo_list(request):
    return render(request, "dashboard/seo/list.html")


def page_list(request):
    return render(request, "dashboard/pages/list.html")
