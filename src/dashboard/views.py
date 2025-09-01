from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from django.db import IntegrityError, transaction
from cinema.models import Cinema, SeoBlock, Movie, Hall, Image
from dashboard.models import (
    Page,
    MainPage,
    ContactPage,
    MainUpperBanner,
    BgBanner,
    NewsPromoBanner,
    BannerImage,
)
from promotion.models import PromoNews

from dashboard.forms import (
    PageForm,
    MainPageForm,
    ContactPageForm,
    CinemaForm,
    SeoBlockForm as PageSeoForm,
)

from .forms_cinema import CinemaCardForm, ImageFormSet, HallForm, HallGalleryFormSet

from .forms_movies import MovieForm, SeoBlockForm as MovieSeoForm, ImageFormSet
from .forms_banners import UpperBannerForm, NewsBannerForm, BgBannerForm

from .forms_news import NewsForm, SeoBlockForm
from django.contrib import messages
from django.urls import reverse
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator


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
        seo_form = PageSeoForm(
            request.POST, instance=page.seo if page and page.seo else None
        )
        initial_qs = page.gallery.all() if page else Image.objects.none()
        img_fs = ImageFormSet(
            request.POST, request.FILES, queryset=initial_qs, prefix="gallery"
        )

        if not page_form.is_valid():
            print(page_form.errors)
        if not seo_form.is_valid():
            print(seo_form.errors)
        if not img_fs.is_valid():
            print(img_fs.non_form_errors())

            for i, f in enumerate(img_fs.forms):
                if f.errors:
                    print(f"img_fs[{i}]:", f.errors)

        if page_form.is_valid() and seo_form.is_valid() and img_fs.is_valid():
            try:
                with transaction.atomic():
                    seo = seo_form.save()
                    page_obj = page_form.save(commit=False)
                    page_obj.seo = seo
                    page_obj.language = lang
                    page_obj.slug = page_form.cleaned_data["slug"]
                    page_obj.save()

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

                # return redirect(f"{request.path}?lang={lang}")
                url = reverse("dashboard:page_edit", args=[slug])
                if lang:
                    url += f"?lang={lang}"
                return redirect(url)

            except Exception as e:
                print("ERROR:", e)

    else:
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
        ContactPage.objects.filter(language=language)
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
    upper_qs = MainUpperBanner.objects.all()
    news_qs = NewsPromoBanner.objects.order_by("position")
    bg_obj, _ = BgBanner.objects.get_or_create(pk=1)

    UpperFS = modelformset_factory(
        MainUpperBanner,
        form=UpperBannerForm,
        can_delete=True,
        extra=1,
        max_num=upper_qs.count() + 1,
        validate_max=True,
    )
    NewsFS = modelformset_factory(
        NewsPromoBanner,
        form=NewsBannerForm,
        can_delete=True,
        extra=1,
        max_num=news_qs.count() + 1,
        validate_max=True,
    )

    if request.method == "POST":
        section = request.POST.get("_section")

        if section == "upper":
            upper_formset = UpperFS(
                request.POST, request.FILES, queryset=upper_qs, prefix="upper"
            )
            if upper_formset.is_valid():
                for form in upper_formset:
                    if not form.has_changed() and not form.cleaned_data.get("DELETE"):
                        continue

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
            news_formset = NewsFS(
                request.POST, request.FILES, queryset=news_qs, prefix="news"
            )
            if news_formset.is_valid():
                for form in news_formset:
                    if not form.has_changed() and not form.cleaned_data.get("DELETE"):
                        continue

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

        elif section == "bg":
            if "remove_bg" in request.POST:
                if bg_obj.image:
                    bg_obj.image.delete(save=True)
                bg_obj.is_image_background = (
                    request.POST.get("bg-background_type") == "image"
                )
                bg_obj.save()
                return redirect("dashboard:banners")

            bg_form = BgBannerForm(
                request.POST, request.FILES, instance=bg_obj, prefix="bg"
            )
            if bg_form.is_valid():
                bg = bg_form.save(commit=False)
                bg.is_image_background = (
                    request.POST.get("bg-background_type") == "image"
                )
                bg.save()
                return redirect("dashboard:banners")

    upper_formset = UpperFS(queryset=upper_qs, prefix="upper")
    news_formset = NewsFS(queryset=news_qs, prefix="news")
    bg_form = BgBannerForm(instance=bg_obj, prefix="bg")

    return render(
        request,
        "dashboard/promotion/banners.html",
        {
            "upper_formset": upper_formset,
            "news_formset": news_formset,
            "bg_form": bg_form,
        },
    )


### Movies =================================================
def movies_list(request):
    current = Movie.objects.filter(is_coming_soon=False).order_by(
        "-release_date", "title"
    )
    soon = Movie.objects.filter(is_coming_soon=True).order_by("release_date", "title")
    return render(
        request, "dashboard/cinema/movies.html", {"current": current, "soon": soon}
    )


@transaction.atomic
def movie_create(request):
    movie_form = MovieForm(request.POST or None, request.FILES or None)
    image_formset = ImageFormSet(
        request.POST or None, request.FILES or None, queryset=Image.objects.none()
    )
    seo_form = MovieSeoForm(request.POST or None)

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
        },
    )


@transaction.atomic
def movie_edit(request, slug):
    movie = get_object_or_404(Movie, slug=slug)

    movie_form = MovieForm(request.POST or None, request.FILES or None, instance=movie)
    seo_form = MovieSeoForm(
        request.POST or None,
        instance=movie.seo if getattr(movie, "seo", None) else None,
    )

    image_formset = ImageFormSet(
        request.POST or None,
        request.FILES or None,
        queryset=movie.gallery.all(),
    )

    if request.method == "POST":
        if movie_form.is_valid() and image_formset.is_valid() and seo_form.is_valid():
            seo_block = seo_form.save()
            mv = movie_form.save(commit=False)
            mv.seo = seo_block
            mv.save()
            movie = mv

            for f in image_formset:
                if not f.cleaned_data:
                    continue

                if f.cleaned_data.get("DELETE") and f.instance.pk:
                    movie.gallery.remove(f.instance)
                    continue

                image_obj = f.save()
                movie.gallery.add(image_obj)

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
            "movie": movie,
        },
    )


### Cinemas =================================================
LANGS = {"ru", "uk"}


def lang_(request):
    lang = request.GET.get("lang") or request.POST.get("lang") or "uk"
    return lang if lang in LANGS else "uk"


def cinemas_list(request):
    lang = lang_(request)
    cinemas = Cinema.objects.select_related("seo").order_by("name")
    return render(
        request,
        "dashboard/cinema/cinemas_list.html",
        {"cinemas": cinemas, "language": lang},
    )


@transaction.atomic
def cinema_create(request):
    lang = lang_(request)

    if request.method == "POST":
        form = CinemaCardForm(request.POST, request.FILES)
        img_fs = ImageFormSet(
            request.POST, request.FILES, queryset=Image.objects.none(), prefix="gallery"
        )

        if not form.is_valid():
            print(form.errors)
        if not img_fs.is_valid():
            print(img_fs.non_form_errors())
            for i, f in enumerate(img_fs.forms):
                if f.errors:
                    print(f"img_fs {i} errors:", f.errors)

        if form.is_valid() and img_fs.is_valid():
            cinema = form.save(commit=False)
            if not cinema.slug:
                cinema.slug = slugify(cinema.name or "")
            cinema.save()

            for f in img_fs:
                if not f.cleaned_data or f.cleaned_data.get("DELETE"):
                    continue

                img = f.save(commit=False)
                if img.image:
                    img.save()
                    cinema.gallery.add(img)

                cinema.save()

            return redirect(
                f"{reverse('dashboard:cinema_edit', kwargs={'slug': cinema.slug})}?lang={lang}"
            )

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
    lang = lang_(request)
    cinema = get_object_or_404(Cinema, slug=slug)

    # Зал create
    if request.method == "POST" and request.POST.get("action") == "create_hall":
        halls_qs = Hall.objects.filter(cinema=cinema)
        default_name = request.POST.get("name") or f"Зал {halls_qs.count() + 1}"

        seo = SeoBlock.objects.create(
            title="",
            description="",
            keywords="",
            slug=slugify(f"hall-{cinema.slug}-{halls_qs.count() + 1}"),
        )
        hall = Hall.objects.create(
            cinema=cinema,
            name=default_name,
            rows=0,
            is_vip=False,
            seo=seo,
        )

        return redirect(
            f"{reverse('dashboard:hall_edit', kwargs={'cinema_slug': cinema.slug, 'pk': hall.pk})}?lang={lang}"
        )

    # Кинотеатр edit
    if request.method == "POST":
        form = CinemaCardForm(request.POST, request.FILES, instance=cinema)
        img_fs = ImageFormSet(
            request.POST, request.FILES, queryset=cinema.gallery.all(), prefix="gallery"
        )

        if form.is_valid() and img_fs.is_valid():
            cinema = form.save()
            for f in img_fs:
                if not getattr(f, "cleaned_data", None):
                    continue
                if f.cleaned_data.get("DELETE") and f.instance.pk:
                    cinema.gallery.remove(f.instance)
                    f.instance.delete()
                    continue
                if not f.instance.pk and not f.cleaned_data.get("image"):
                    continue
                img_obj = f.save()
                cinema.gallery.add(img_obj)

            return redirect(
                f"{reverse('dashboard:cinema_edit', kwargs={'slug': cinema.slug})}?lang={lang}"
            )
    else:
        form = CinemaCardForm(instance=cinema)
        img_fs = ImageFormSet(queryset=cinema.gallery.all(), prefix="gallery")

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

    cinema.delete()

    return redirect(
        f"{reverse('dashboard:cinemas_list')}?lang={lang}"
        if lang
        else reverse("dashboard:cinemas_list")
    )


# def halls_list(request, cinema_slug):
#     lang = lang_(request)
#     cinema = get_object_or_404(Cinema, slug=cinema_slug)
#     halls = Hall.objects.filter(cinema=cinema).order_by("name")
#     return render(
#         request,
#         "dashboard/cinema/halls_list.html",
#         {"cinema": cinema, "halls": halls, "language": lang},
#     )


@transaction.atomic
def hall_delete(request, cinema_slug, pk):
    cinema = get_object_or_404(Cinema, slug=cinema_slug)
    hall = get_object_or_404(Hall, pk=pk, cinema=cinema)

    if request.method == "POST":
        hall.delete()
        return redirect(
            f"{reverse('dashboard:cinema_edit', kwargs={'slug': cinema.slug})}?lang={lang_(request)}"
        )

    return render(
        request,
        "dashboard/cinema/hall_confirm_delete.html",
        {
            "cinema": cinema,
            "hall": hall,
        },
    )


@transaction.atomic
def hall_create(request, cinema_slug):
    lang = lang_(request)
    cinema = get_object_or_404(Cinema, slug=cinema_slug)

    if request.method == "POST":
        form = HallForm(request.POST, request.FILES)
        img_fs = HallGalleryFormSet(
            request.POST, request.FILES, queryset=Image.objects.none(), prefix="gallery"
        )

        if form.is_valid() and img_fs.is_valid():
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

            # галерея
            for f in img_fs:
                if not getattr(f, "cleaned_data", None):
                    continue
                if f.cleaned_data.get("DELETE"):
                    continue
                img = f.save(commit=False)
                if not img.image:
                    continue
                img.save()
                hall.gallery.add(img)

            return redirect(
                f"{reverse('dashboard:hall_edit', kwargs={'cinema_slug': cinema.slug, 'pk': hall.pk})}?lang={lang}"
            )

    else:
        form = HallForm()
        img_fs = HallGalleryFormSet(queryset=Image.objects.none(), prefix="gallery")

    return render(
        request,
        "dashboard/cinema/hall_form.html",
        {
            "form": form,
            "img_fs": img_fs,
            "cinema": cinema,
            "hall": None,
            "language": lang,
        },
    )


@transaction.atomic
def hall_edit(request, cinema_slug, pk):
    lang = lang_(request)
    cinema = get_object_or_404(Cinema, slug=cinema_slug)
    hall = get_object_or_404(Hall, pk=pk, cinema=cinema)

    if request.method == "POST":
        form = HallForm(request.POST, request.FILES, instance=hall)
        img_fs = HallGalleryFormSet(
            request.POST, request.FILES, queryset=hall.gallery.all(), prefix="gallery"
        )

        if form.is_valid() and img_fs.is_valid():
            hall = form.save()

            for f in img_fs:
                if not getattr(f, "cleaned_data", None):
                    continue

                if f.cleaned_data.get("DELETE") and f.instance.pk:
                    hall.gallery.remove(f.instance)
                    f.instance.delete()
                    continue

                img = f.save(commit=False)
                if not img.pk and not img.image:
                    continue
                img.save()
                hall.gallery.add(img)

            return redirect(
                f"{reverse('dashboard:hall_edit', kwargs={'cinema_slug': cinema.slug, 'pk': hall.pk})}?lang={lang}"
            )

    else:
        form = HallForm(instance=hall)
        img_fs = HallGalleryFormSet(queryset=hall.gallery.all(), prefix="gallery")

    return render(
        request,
        "dashboard/cinema/hall_form.html",
        {
            "form": form,
            "img_fs": img_fs,
            "cinema": cinema,
            "hall": hall,
            "language": lang,
        },
    )


def news_list(request, lang=None):
    qs = (
        PromoNews.objects.select_related("seo")
        .prefetch_related("gallery")
        .filter(is_active=True)
        .defer("text")
        .order_by("-published_at", "-id")
    )

    q = request.GET.get("q")
    if q:
        qs = qs.filter(title__icontains=q)

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    return render(
        request,
        "dashboard/promotion/news_list.html",
        {"news": page_obj, "page_obj": page_obj, "lang": lang},
    )


def _unique_slug(model, base: str) -> str:
    s = slugify(base or "") or "item"
    orig, i = s, 2
    while model.objects.filter(slug=s).exists():
        s = f"{orig}-{i}"
        i += 1
    return s


def news_create(request, lang=None):
    if request.method == "POST":
        news_form = NewsForm(request.POST, request.FILES)
        seo_form = SeoBlockForm(request.POST)
        formset = ImageFormSet(
            request.POST, request.FILES, queryset=Image.objects.none(), prefix="gallery"
        )
        if news_form.is_valid() and seo_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                seo = seo_form.save()
                instance = news_form.save(commit=False)
                if not instance.slug:
                    instance.slug = _unique_slug(PromoNews, instance.title)
                if not instance.type:
                    instance.type = "news"
                instance.seo = seo
                instance.save()

                images_to_add = []
                for f in formset.forms:
                    if not f.cleaned_data or f.cleaned_data.get("DELETE"):
                        continue
                    images_to_add.append(f.save())

                if images_to_add:
                    instance.gallery.add(*images_to_add)

                messages.success(request, "Новость создана.")
                return redirect("news:list")
        else:
            messages.error(request, "Исправьте ошибки формы.")
    else:
        news_form = NewsForm()
        seo_form = SeoBlockForm()
        formset = ImageFormSet(queryset=Image.objects.none(), prefix="gallery")

    return render(
        request,
        "dashboard/promotion/news_create.html",
        {"form": news_form, "seo_form": seo_form, "formset": formset, "mode": "create"},
    )


def news_edit(request, lang=None, pk=None, slug=None):
    lookup = {"pk": pk} if pk is not None else {"slug": slug}
    obj = get_object_or_404(
        PromoNews.objects.select_related("seo").prefetch_related("gallery"), **lookup
    )

    if request.method == "POST":
        news_form = NewsForm(request.POST, request.FILES, instance=obj)
        seo_form = SeoBlockForm(request.POST, instance=obj.seo)
        formset = ImageFormSet(
            request.POST, request.FILES, queryset=obj.gallery.all(), prefix="gallery"
        )
        if news_form.is_valid() and seo_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                seo = seo_form.save()
                instance = news_form.save(commit=False)
                if not instance.slug:
                    instance.slug = _unique_slug(PromoNews, instance.title)
                instance.seo = seo
                instance.save()

                keep = []
                for f in formset.forms:
                    if not f.cleaned_data:
                        continue
                    if f.cleaned_data.get("DELETE"):
                        if f.instance.pk:
                            obj.gallery.remove(f.instance)
                            f.instance.delete()
                        continue
                    keep.append(f.save())

                obj.gallery.set(keep)

                messages.success(request, "Новость обновлена.")
                return redirect("news:list")
        else:
            messages.error(request, "Исправьте ошибки формы.")
    else:
        news_form = NewsForm(instance=obj)
        seo_form = SeoBlockForm(instance=obj.seo)
        formset = ImageFormSet(queryset=obj.gallery.all(), prefix="gallery")

    return render(
        request,
        "dashboard/promotion/news_create.html",
        {
            "form": news_form,
            "seo_form": seo_form,
            "formset": formset,
            "mode": "edit",
            "object": obj,
        },
    )
