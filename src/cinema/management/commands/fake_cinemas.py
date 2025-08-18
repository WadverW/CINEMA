from django.core.management.base import BaseCommand
from faker import Faker
from cinema.models import SeoBlock, Image, Cinema, Hall, Movie
import random
from datetime import timedelta, date

fake = Faker("ru_RU")


class Command(BaseCommand):
    help = "Загружает фейковые данные для моделей Cinema, Hall, Movie"

    def handle(self, *args, **kwargs):
        self.create_seo_blocks()
        self.create_images()
        self.create_cinemas_and_halls()
        self.create_movies()
        self.stdout.write(self.style.SUCCESS("✅ Данные успешно загружены"))

    def create_seo_blocks(self, count=20):
        self.seo_blocks = []
        for _ in range(count):
            seo = SeoBlock.objects.create(
                title=fake.sentence(),
                description=fake.text(),
                keywords=fake.words(nb=5, ext_word_list=None),
                slug=fake.slug(),
            )
            self.seo_blocks.append(seo)

    def create_images(self, count=10):
        self.images = []
        for _ in range(count):
            image = Image.objects.create(
                image=None,  # загрузи вручную или через админку
                alt_text=fake.sentence(),
            )
            self.images.append(image)

    def create_cinemas_and_halls(self, count=5):
        self.cinemas = []
        for i in range(count):
            cinema = Cinema.objects.create(
                name=fake.company(),
                slug=fake.slug(),
                city=fake.city(),
                address=fake.address(),
                phone_number=fake.phone_number(),
                description=fake.text(),
                map_coordinates=f"{fake.latitude()},{fake.longitude()}",
                image=None,
                seo=random.choice(self.seo_blocks),
            )
            self.cinemas.append(cinema)
            # создаем залы
            for j in range(random.randint(1, 3)):
                Hall.objects.create(
                    cinema=cinema,
                    name=f"Зал {j + 1}",
                    rows=random.randint(5, 15),
                    is_vip=random.choice([True, False]),
                    seo=random.choice(self.seo_blocks),
                    map_hall=None,
                )

    def create_movies(self, count=10):
        for _ in range(count):
            movie = Movie.objects.create(
                title=fake.sentence(nb_words=3),
                slug=fake.slug(),
                description=fake.text(max_nb_chars=400),
                poster=None,
                trailer_url=f"https://www.youtube.com/watch?v={fake.pystr(min_chars=11, max_chars=11)}",
                age_rating=random.choice(["0+", "6+", "12+", "16+", "18+"]),
                release_date=fake.date_between(start_date="-1y", end_date="+3m"),
                is_coming_soon=random.choice([True, False]),
                is_2d=random.choice([True, False]),
                is_3d=random.choice([True, False]),
                is_imax=random.choice([True, False]),
                seo=random.choice(self.seo_blocks),
            )
            # Добавить картинки в галерею
            movie.gallery.set(random.sample(self.images, random.randint(1, 3)))
