from faker import Faker
from users.models import User

fake = Faker("ru_RU")


def run():
    for _ in range(10):
        User.objects.create(
            username=fake.unique.user_name(),
            phone_number=fake.phone_number(),
            birth=fake.date_of_birth(minimum_age=18, maximum_age=60),
            city=fake.city(),
            gender="male" if fake.boolean() else "female",
            language="ru",
            card_number=fake.credit_card_number(),
            nickname=fake.user_name(),
        )
    print("Users added")
