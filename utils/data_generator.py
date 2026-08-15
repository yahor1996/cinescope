import random
import string
from faker import Faker


faker = Faker()


class DataGenerator:

    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_firstname():
        return faker.first_name()

    @staticmethod
    def generate_lastname():
        return faker.last_name()

    @staticmethod
    def generate_valid_password():
        # Обязательные части
        letter = random.choice(string.ascii_letters)  # хотя бы одна буква
        digit = random.choice(string.digits)  # хотя бы одна цифра
        special_chars = "?@#$%^&*_-+()[]{}\\/|\"',.:"  # разрешённые спецсимволы
        spec = random.choice(special_chars)  # хотя бы один спецсимвол (если нужен)

        # Все разрешённые символы
        all_allowed = string.ascii_letters + string.digits + special_chars

        length = 12  # длина между 8 и 20
        remaining = length - 3  # минус letter, digit, spec
        rest = ''.join(random.choice(all_allowed) for _ in range(remaining))

        password = list(letter + digit + spec + rest)
        random.shuffle(password)
        return ''.join(password)

    @staticmethod
    def generate_genreId():
        return faker.random_int(1, 1)

    @staticmethod
    def generate_page():
        return random.randint(1, 2)

    @staticmethod
    def generate_page_size():
        return random.randint(1, 5)

    @staticmethod
    def generate_movie_name():
        return (
                "movie"
                + faker.first_name()
                + faker.last_name()
                + str(faker.random_int(1, 1000))
        )

    @staticmethod
    def generate_image_url():
        return faker.image_url()

    @staticmethod
    def generate_movie_price():
        return faker.random_int(min=100, max=1000)

    @staticmethod
    def generate_movie_description():
        return faker.text(max_nb_chars=200)

    @staticmethod
    def generate_movie_location():
        return faker.random_element(["MSK", "SPB"])

    @staticmethod
    def generate_movie_is_published():
        return faker.boolean()

    @staticmethod
    def generate_wrong_movie_id():
        return faker.random_int(min=100000000, max=900000000)

    @staticmethod
    def generate_prefix_email():
        return faker.random_int(min=1, max=1000)