from django.shortcuts import get_object_or_404, render


def home(request):
    cards = range(8)
    return render(request, "home.html", {"cards": cards})


def afisha(request):
    movies = range(18)
    return render(request, "cinema/afisha.html", {"movies": movies})


def movie_detail(request):
    days = ["18", "19", "20", "21", "22", "23", "24"]
    return render(request, "cinema/movie_detail.html", {"days": days})


def soon(request):
    movies = range(18)
    return render(request, "cinema/soon.html", {"movies": movies})


def schedule(request):
    days = ["18", "19", "20", "21", "22", "23", "24"]
    # selected_date = request.GET.get('date')
    # if selected_date:
    #     schedule = Screening.objects.filter(date=selected_date)
    # else:
    #     schedule = Screening.objects.all()
    schedule = [
        {"time": "10:10", "title": "Фильм 1", "hall": 1, "price": 50},
        {"time": "11:20", "title": "Фильм 2", "hall": 2, "price": 55},
        {"time": "12:30", "title": "Фильм 3", "hall": 3, "price": 60},
        {"time": "13:40", "title": "Фильм 4", "hall": 4, "price": 65},
        {"time": "14:50", "title": "Фильм 5", "hall": 5, "price": 70},
        {"time": "16:00", "title": "Фильм 6", "hall": 6, "price": 75},
        {"time": "17:10", "title": "Фильм 7", "hall": 7, "price": 80},
    ]
    return render(request, "cinema/schedule.html", {"days": days, "schedule": schedule})


def cinemas(request):
    theatres = range(6)
    return render(request, "cinema/cinemas.html", {"theatres": theatres})


def cinema_detail(request):
    return render(request, "cinema/cinema_detail.html")


def hall_detail(request):
    return render(request, "cinema/hall_detail.html")


def promos(request):
    return render(request, "cinema/promos.html")


def about_cinema(request):
    return render(request, "cinema/about_cinema.html")


# about cinema links
def news(request):
    return render(request, "cinema/about_cinema/news.html")


def advertise(request):
    return render(request, "cinema/about_cinema/advertise.html")


def cafe(request):
    return render(request, "cinema/about_cinema/cafe.html")


def mobile_apps(request):
    return render(request, "cinema/about_cinema/mobile_apps.html")


def contacts(request):
    return render(request, "cinema/about_cinema/contacts.html")
