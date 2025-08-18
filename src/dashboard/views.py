from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from django.db import IntegrityError, transaction
from cinema.models import Cinema, SeoBlock, Movie, Hall, Image
from dashboard.models import (
    Page, MainPage, ContactPage, MainUpperBanner, BgBanner, NewsPromoBanner, BannerImage
    )

from dashboard.forms import (
    PageForm, MainPageForm, ContactPageForm, CinemaForm, SeoBlockForm as PageSeoForm
)

from .forms_cinema import CinemaCardForm, ImageFormSet, HallForm

from .forms_movies import MovieForm, SeoBlockForm as MovieSeoForm, ImageFormSet
from .forms_banners import UpperBannerForm, NewsBannerForm, BgBannerForm
from .forms import ImageFormSet
from django.contrib import messages
from django.urls import reverse
from django.utils.text import slugify
from django.views.decorators.http import require_POST

def index(request):
    return render(request, "dashboard/index.html")
### Pages
# MainPage ===================================================
def main_page(request):
    language = request.GET.get("lang", "ru")
    main_page = MainPage.objects.select_related("seo").filter(language=language).first()

    if request.method == "POST":
        main_form = MainPageForm(request.POST, instance=main_page)
        seo_form = PageSeoForm(
            request.POST,
            instance=main_page.seo if main_page and main_page.seo else None,
        )

        if main_form.is_valid() and seo_form.is_valid():
            with transaction.atomic():
                seo = seo_form.save()
                main_page = main_form.save(commit=False)
                main_page.seo = seo
                main_page.language = language
                main_page.save()
            return redirect(f"{request.path}?lang={language}")

    else:
        main_form = MainPageForm(instance=main_page)
        seo_form = PageSeoForm(instance=main_page.seo if main_page else None)

    context = {
        "main_form": main_form,
        "seo_form": seo_form,
        "language": language,
    }
    return render(request, "dashboard/pages/main_page.html", context)


### Page ===================================================
LANGS = {"ru", "uk"}

def page_edit(request, slug):
    lang = request.GET.get("lang") or request.session.get("lang", "ru")
    if lang not in LANGS:
        lang = "ru"
    request.session["lang"] = lang

    page = Page.objects.select_related("seo").filter(slug=slug, language=lang).first()
    existed_before = page is not None

    if request.method == "POST":
        print(f"[page_edit] POST slug={slug}, lang={lang}")

        page_form = PageForm(request.POST, request.FILES, instance=page)
        seo_form = PageSeoForm(request.POST, instance=page.seo if page and page.seo else None)
        initial_qs = page.gallery.all() if page else Image.objects.none()
        img_fs = ImageFormSet(request.POST, request.FILES, queryset=initial_qs, prefix="gallery")

        if not page_form.is_valid():
            print("[page_edit] page_form INVALID:", page_form.errors)
        if not seo_form.is_valid():
            print("[page_edit] seo_form INVALID:", seo_form.errors)
        if not img_fs.is_valid():
            print("[page_edit] img_fs INVALID (non_form):", img_fs.non_form_errors())
            # Покажем ошибки по кажой форме формсета (кратко)
            for i, f in enumerate(img_fs.forms):
                if f.errors:
                    print(f"[page_edit] img_fs[{i}] errors:", f.errors)

        if page_form.is_valid() and seo_form.is_valid() and img_fs.is_valid():
            try:
                with transaction.atomic():
                    seo = seo_form.save()
                    page_obj = page_form.save(commit=False)
                    page_obj.seo = seo
                    page_obj.language = lang
                    page_obj.slug = page_form.cleaned_data["slug"]
                    page_obj.save()

                    # простая обработка формсета
                    for f in img_fs.forms:
                        if not getattr(f, "cleaned_data", None):
                            continue
                        if f.cleaned_data.get("DELETE") and f.instance.pk:
                            page_obj.gallery.remove(f.instance)
                            f.instance.delete()
                            continue
                        img = f.save(commit=False)
                        if not img.pk and not img.image:
                            continue
                        img.save()
                        page_obj.gallery.add(img)

                print(f"[page_edit] OK: {'created' if not existed_before else 'updated'} page id={page_obj.id}")
                return redirect(f"{request.path}?lang={lang}")

            except Exception as e:
                print("[page_edit] ERROR while saving:", e)

        # Если дошли сюда — была ошибка, просто падаем в рендер ниже

    else:
        print(f"[page_edit] GET slug={slug}, lang={lang}")
        page_form = PageForm(instance=page)
        seo_form = PageSeoForm(instance=page.seo if page else None)
        initial_qs = page.gallery.all() if page else Image.objects.none()
        img_fs = ImageFormSet(queryset=initial_qs, prefix="gallery")

    return render(
        request,
        "dashboard/pages/page_form.html",
        {
            "page_form": page_form,
            "seo_form": seo_form,
            "img_fs": img_fs,
            "language": lang,
            "slug": slug,
        },
    )

### Contact Page ===================================================
def contact_page(request):
    language = request.GET.get("lang", "ru")

    page = (
        ContactPage.objects
        .filter(language=language)
        .select_related("cinema", "seo")
        .first()
    )

    if not page:
        seo = SeoBlock.objects.create(
            title="",
            description="",
            keywords="",
            slug=f"contacts-{language}",
        )
        cinema = Cinema.objects.create(
            name="",
            slug=f"cinema-{language}",
            city="",
            address="",
            phone_number="",
            description="",
            map_coordinates="",
            seo=seo,
        )
        page = ContactPage.objects.create(
            is_active=True,
            language=language,
            cinema=cinema,
            seo=seo,
        )

    if request.method == "POST":
        contact_form = ContactPageForm(request.POST, instance=page)
        cinema_form = CinemaForm(request.POST, request.FILES, instance=page.cinema)
        seo_form = PageSeoForm(request.POST, instance=page.seo)

        if contact_form.is_valid() and cinema_form.is_valid() and seo_form.is_valid():
            try:
                with transaction.atomic():
                    seo_obj = seo_form.save()

                    cinema_obj = cinema_form.save(commit=False)
                    cinema_obj.seo = seo_obj
                    cinema_obj.save()

                    cp = contact_form.save(commit=False)
                    cp.language = language
                    cp.cinema = cinema_obj
                    cp.seo = seo_obj
                    cp.save()

                messages.success(request, "Контакты сохранены!")
                return redirect(f"{request.path}?lang={language}")

            except Exception as e:
                messages.error(request, f"Ошибка при сохранении -> {e}")
        else:
           messages.error(request, "Проблема валидации форм!")

    else:
        contact_form = ContactPageForm(instance=page)
        cinema_form = CinemaForm(instance=page.cinema)
        seo_form = PageSeoForm(instance=page.seo)

    return render(
        request,
        "dashboard/pages/contact_page.html",
        {
            "contact_form": contact_form,
            "cinema_form": cinema_form,
            "seo_form": seo_form,
            "language": language,
        },
    )


### Banners ===================================================
def banners(request):
    upper_qs = MainUpperBanner.objects.order_by("position")
    news_qs = NewsPromoBanner.objects.order_by("position")
    bg_obj, _ = BgBanner.objects.get_or_create(pk=1)

    upper_fs = modelformset_factory(
        MainUpperBanner,
        form=UpperBannerForm,
        can_delete=True,
        extra=1,
        max_num=upper_qs.count() + 1,
        validate_max=True,
)
    news_fs = modelformset_factory(
        NewsPromoBanner,
        form=NewsBannerForm,
        can_delete=True,
        extra=1,
        max_num=news_qs.count() + 1,
        validate_max=True,
    )

    if request.method == "POST":
        section = request.POST.get("section_")

        if section == "upper":
            upper_formset = upper_fs(request.POST, request.FILES, queryset=upper_qs, prefix="upper")
            if upper_formset.is_valid():
                for form in upper_formset:
                    if form.cleaned_data.get("DELETE"):
                        if form.instance.pk:
                            form.instance.delete()
                        continue
                    banner = form.save()
                    img_file = form.cleaned_data.get("image_file")
                    if img_file:
                        bi = BannerImage.objects.create(image=img_file)
                        banner.image.add(bi)
                return redirect("dashboard:banners")

        elif section == "news":
            news_formset = news_fs(request.POST, request.FILES, queryset=news_qs, prefix="news")
            if news_formset.is_valid():
                for form in news_formset:
                    if form.cleaned_data.get("DELETE"):
                        if form.instance.pk:
                            form.instance.delete()
                        continue
                    banner = form.save()
                    img_file = form.cleaned_data.get("image_file")
                    if img_file:
                        bi = BannerImage.objects.create(image=img_file)
                        banner.image.add(bi)
                return redirect("dashboard:banners")

        if section == "bg":
            if "remove_bg" in request.POST:
                if bg_obj.image:
                    bg_obj.image.delete(save=True)
                bg_obj.is_image_background = (request.POST.get("bg-background_type") == "image")
                bg_obj.save()
                return redirect("dashboard:banners")

            bg_form = BgBannerForm(request.POST, request.FILES, instance=bg_obj, prefix="bg")
            if bg_form.is_valid():
                bg = bg_form.save(commit=False)
                bg.is_image_background = (request.POST.get("bg-background_type") == "image")
                bg.save()
                return redirect("dashboard:banners")

    upper_formset = upper_fs(queryset=upper_qs, prefix="upper")
    news_formset = news_fs(queryset=news_qs, prefix="news")
    bg_form = BgBannerForm(instance=bg_obj, prefix="bg")

    return render(
        request,
        "dashboard/promotion/banners.html",
        {"upper_formset": upper_formset, "news_formset": news_formset, "bg_form": bg_form},
    )


### Movies =================================================
def movies_list(request):
    current = Movie.objects.filter(is_coming_soon=False).order_by("-release_date", "title")
    soon = Movie.objects.filter(is_coming_soon=True).order_by("release_date", "title")
    return render(request, "dashboard/cinema/movies.html", {"current": current, "soon": soon})

@transaction.atomic
def movie_create(request):
    movie_form = MovieForm(request.POST or None, request.FILES or None)
    image_formset = ImageFormSet(request.POST or None, request.FILES or None, queryset=Image.objects.none())
    seo_form =  MovieSeoForm(request.POST or None)

    if request.method == "POST":
        if movie_form.is_valid() and image_formset.is_valid() and seo_form.is_valid():
            seo_block = seo_form.save()
            movie = movie_form.save(commit=False)
            movie.seo = seo_block
            movie.save()

            for img_form in image_formset:
                if img_form.cleaned_data:
                    image = img_form.save()
                    movie.gallery.add(image)

            return redirect("dashboard:movies_list")
        else:
            print("Movie form errors:", movie_form.errors)
            print("Image formset errors:", image_formset.errors)
            print("SEO form errors:", seo_form.errors)

    return render(
        request,
        "dashboard/cinema/movie_create.html",
        {
            "movie_form": movie_form,
            "image_formset": image_formset,
            "seo_form": seo_form,
        }
    )


### Cinemas =================================================
LANGS = {"ru", "uk"}

def _lang(request):
    lang = request.GET.get("lang") or request.POST.get("lang") or "ru"
    return lang if lang in LANGS else "ru"


def cinemas_list(request):
    """Список кинотеатров."""
    lang = _lang(request)
    cinemas = Cinema.objects.select_related("seo").order_by("name")
    return render(
        request,
        "dashboard/cinema/cinemas_list.html",
        {"cinemas": cinemas, "language": lang},
    )


@transaction.atomic
def cinema_create(request):
    """Создание кинотеатра: поля + логотип + галерея (formset)."""
    lang = _lang(request)

    if request.method == "POST":
        form = CinemaCardForm(request.POST, request.FILES)
        img_fs = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none(), prefix="gallery")

        if not form.is_valid():
            print("[cinema_create] form INVALID:", form.errors)
        if not img_fs.is_valid():
            print("[cinema_create] img_fs INVALID:", img_fs.non_form_errors())
            for i, f in enumerate(img_fs.forms):
                if f.errors:
                    print(f"[cinema_create] img_fs[{i}] errors:", f.errors)

        if form.is_valid() and img_fs.is_valid():
            cinema = form.save(commit=False)
            if not cinema.slug:
                cinema.slug = slugify(cinema.name or "")
            cinema.save()

            # галерея
            for f in img_fs.forms:
                if not getattr(f, "cleaned_data", None):
                    continue
                if f.cleaned_data.get("DELETE") and f.instance.pk:
                    continue  # при создании вряд ли понадобится
                img = f.save(commit=False)
                if not img.pk and not img.image:
                    continue  # пустой слот
                img.save()
                cinema.gallery.add(img)

            url = reverse("dashboard:cinema_edit", kwargs={"slug": cinema.slug})
            return redirect(f"{url}?lang={lang}")

    else:
        form = CinemaCardForm()
        img_fs = ImageFormSet(queryset=Image.objects.none(), prefix="gallery")

    return render(
        request,
        "dashboard/cinema/cinema_form.html",
        {"cinema_form": form, "img_fs": img_fs, "language": lang},
    )


@transaction.atomic
def cinema_edit(request, slug):
    """
    Редактирование кинотеатра:
    - основные поля (CinemaCardForm)
    - логотип (в форме)
    - галерея через ImageFormSet (prefix='gallery')
    - таблица залов внизу страницы
    """
    lang = _lang(request)
    cinema = get_object_or_404(Cinema, slug=slug)

    if request.method == "POST":
        form = CinemaCardForm(request.POST, request.FILES, instance=cinema)
        img_fs = ImageFormSet(
            request.POST, request.FILES,
            queryset=cinema.gallery.all(),
            prefix="gallery"
        )

        # Быстрые отладочные принты
        if not form.is_valid():
            print("[cinema_edit] form INVALID:", form.errors)
        if not img_fs.is_valid():
            print("[cinema_edit] img_fs INVALID (non_form):", img_fs.non_form_errors())
            for i, f in enumerate(img_fs.forms):
                if f.errors:
                    print(f"[cinema_edit] img_fs[{i}] errors:", f.errors)

        if form.is_valid() and img_fs.is_valid():
            # 1) Сохраняем поля кинотеатра
            cinema = form.save()
            print(f"[cinema_edit] Cinema saved id={cinema.id}, slug={cinema.slug}")

            # 2) Обрабатываем галерею
            for f in img_fs.forms:
                if not getattr(f, "cleaned_data", None):
                    continue

                # Удаление существующей картинки из галереи
                if f.cleaned_data.get("DELETE") and f.instance.pk:
                    print(f"[cinema_edit] delete image id={f.instance.pk}")
                    cinema.gallery.remove(f.instance)
                    # если изображение больше нигде не используется — удаляем объект
                    f.instance.delete()
                    continue

                img = f.save(commit=False)

                # Пустой "слот" без файла — пропускаем
                if not img.pk and not img.image:
                    continue

                img.save()
                cinema.gallery.add(img)
                print(f"[cinema_edit] add/update image id={img.pk}")

            # 3) PRG: редирект на эту же страницу
            url = reverse("dashboard:cinema_edit", kwargs={"slug": cinema.slug})
            return redirect(f"{url}?lang={lang}")

    else:
        form = CinemaCardForm(instance=cinema)
        img_fs = ImageFormSet(queryset=cinema.gallery.all(), prefix="gallery")

    # Таблица залов (всегда считаем для шаблона — он сам решит, что показать)
    halls = Hall.objects.filter(cinema=cinema).order_by("name")

    return render(
        request,
        "dashboard/cinema/cinema_form.html",
        {
            "cinema_form": form,
            "img_fs": img_fs,
            "language": lang,
            "cinema": cinema,
            "halls": halls,
        },
    )

@require_POST
@transaction.atomic
def cinema_delete(request, slug):
    lang = request.GET.get("lang") or request.POST.get("lang") or ""
    cinema = get_object_or_404(Cinema, slug=slug)

    for hall in Hall.objects.filter(cinema=cinema).select_related("seo"):
        if hall.seo:
            hall.seo.delete() 

    seo = cinema.seo if hasattr(cinema, "seo") else None
    cinema.delete()
    if seo:
        seo.delete()

    return redirect(f"{reverse('dashboard:cinemas_list')}?lang={lang}" if lang else reverse("dashboard:cinemas_list"))


def halls_list(request, cinema_slug):
    """Простой список залов конкретного кинотеатра."""
    lang = _lang(request)
    cinema = get_object_or_404(Cinema, slug=cinema_slug)
    halls = Hall.objects.filter(cinema=cinema).order_by("name")
    return render(
        request,
        "dashboard/cinema/halls_list.html",
        {"cinema": cinema, "halls": halls, "language": lang},
    )


@transaction.atomic
def halls_table(request, cinema_slug):
    """GET — таблица залов; POST — создать новый зал и редирект на его редактирование."""
    lang = _lang(request)
    cinema = get_object_or_404(Cinema, slug=cinema_slug)

    if request.method == "POST" and request.POST.get("action") == "create":
        next_num = Hall.objects.filter(cinema=cinema).count() + 1
        default_name = request.POST.get("name") or f"Зал {next_num}"

        seo = SeoBlock.objects.create(
            title="",
            description="",
            keywords="",
            slug=slugify(f"hall-{cinema.slug}-{next_num}"),
        )
        hall = Hall.objects.create(
            cinema=cinema,
            name=default_name,
            rows=0,
            is_vip=False,
            seo=seo,
        )
        url = reverse("dashboard:hall_edit", kwargs={"cinema_slug": cinema.slug, "pk": hall.pk})
        return redirect(f"{url}?lang={lang}")

    halls = Hall.objects.filter(cinema=cinema).order_by("name")
    return render(
        request,
        "dashboard/cinema/halls_table.html",
        {"cinema": cinema, "halls": halls, "language": lang},
    )

@transaction.atomic
def hall_edit(request, cinema_slug, pk):
    """Редактирование существующего зала."""
    cinema = get_object_or_404(Cinema, slug=cinema_slug)
    hall = get_object_or_404(Hall, pk=pk, cinema=cinema)

    if request.method == "POST":
        form = HallForm(request.POST, instance=hall)
        if form.is_valid():
            form.save()
            return redirect("dashboard:halls_table", cinema_slug=cinema.slug)
    else:
        form = HallForm(instance=hall)

    return render(request, "dashboard/cinema/hall_form.html", {
        "form": form,
        "cinema": cinema,
        "hall": hall,
    })


@transaction.atomic
def hall_delete(request, cinema_slug, pk):
    """Удаление зала."""
    cinema = get_object_or_404(Cinema, slug=cinema_slug)
    hall = get_object_or_404(Hall, pk=pk, cinema=cinema)

    if request.method == "POST":
        hall.delete()
        return redirect("dashboard:halls_table", cinema_slug=cinema.slug)

    return render(request, "dashboard/cinema/hall_confirm_delete.html", {
        "cinema": cinema,
        "hall": hall,
    })

@transaction.atomic
def hall_create(request, cinema_slug):
    lang = _lang(request)
    cinema = get_object_or_404(Cinema, slug=cinema_slug)

    if request.method == "POST":
        form = HallForm(request.POST)
        if not form.is_valid():
            print("[hall_create] form INVALID:", form.errors)
        if form.is_valid():
            # создаём SEO для зала
            next_num = Hall.objects.filter(cinema=cinema).count() + 1
            seo = SeoBlock.objects.create(
                title="",
                description="",
                keywords="",
                slug=slugify(f"hall-{cinema.slug}-{next_num}"),
            )
            hall = form.save(commit=False)
            hall.cinema = cinema
            hall.seo = seo
            hall.save()

            url = reverse("dashboard:hall_edit", kwargs={"cinema_slug": cinema.slug, "pk": hall.pk})
            return redirect(f"{url}?lang={lang}")
    else:
        form = HallForm()

    return render(
        request,
        "dashboard/cinema/hall_form.html",  
        {"form": form, "cinema": cinema, "hall": None, "language": lang},
    )

