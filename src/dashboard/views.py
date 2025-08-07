from django.shortcuts import redirect, render
from .forms import SeoForm, CinemaForm, HallForm, NewsForm
from datetime import datetime


def index(request):
    return render(request, "dashboard/index.html")


# # Статистика
# def stats(request):
#     return render(request, "dashboard/stats.html")


def banners(request):
    return render(request, "dashboard/promotion/banners.html")


def movies_admin(request):
    return render(request, "dashboard/cinema/movies_admin.html")


def movies_create(request):
    # seo_form = SeoForm(request.POST or None)

    # if request.method == "POST":
    #     if seo_form.is_valid():
    #         url = seo_form.cleaned_data["seo_url"]
    #         title = seo_form.cleaned_data["seo_title"]
    #         keywords = seo_form.cleaned_data["seo_keywords"]
    #         description = seo_form.cleaned_data["seo_description"]
    #         seo_form = Seo(url=url, title=title, keywords=keywords, description=description)
    #         seo_form.save()

    #         return redirect("dashboard:movies_admin")  # поменяй на нужный URL name

    # return render(
    #     request,
    #     "dashboard/movies/movie_form.html",
    #     {
    #         "seo_form": seo_form,
    #     },
    # )
    return render(request, "dashboard/cinema/movies_create.html")


def cinema_list(request):
    return render(request, "dashboard/cinema/cinemas_admin.html")


def cinema_create(request):
    cinema_form = CinemaForm()
    seo_form = SeoForm()
    return render(
        request,
        "dashboard/cinema/cinemas_create.html",
        {
            "cinema_form": cinema_form,
            "seo_form": seo_form,
        },
    )


def hall_create(request):
    hall_form = HallForm()
    seo_form = SeoForm()
    return render(
        request,
        "dashboard/cinema/hall_create.html",
        {
            "hall_form": hall_form,
            "seo_form": seo_form,
        },
    )


def news_list(request):
    return render(request, "dashboard/promotion/news_admin.html")


def news_create(request):
    form = NewsForm(request.POST or None)

    # if request.method == "POST" and form.is_valid():
    #     # здесь будет сохранение данных в модель
    #     print(form.cleaned_data)
    #     return redirect('dashboard:news_list')

    return render(request, "dashboard/promotion/news_create.html", {"form": form})


def promotions(request):
    return render(request, "dashboard/promotions.html")


# Страницы
def page_main(request):
    return render(request, "dashboard/pages/main.html")


def page_about(request):
    return render(request, "dashboard/pages/about.html")


def page_cafe(request):
    return render(request, "dashboard/pages/cafe.html")


def page_vip(request):
    return render(request, "dashboard/pages/vip.html")


def page_kids(request):
    return render(request, "dashboard/pages/kids.html")


def page_ads(request):
    return render(request, "dashboard/pages/ads.html")


def page_contacts(request):
    return render(request, "dashboard/pages/contacts.html")


# Пользователи
def users(request):
    return render(request, "dashboard/users.html")


# Рассылка
def mailing(request):
    return render(request, "dashboard/mailing.html")
