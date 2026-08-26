from conftest import db_session, TestMovie
from db_models.movies import MovieDBModel
from models.movie_models import MovieCreatedResponse
from utils.data_generator import DataGenerator


class TestDataBase:

    def test_db_requests(self, super_admin, db_helper, created_test_user):
        assert created_test_user == db_helper.get_user_by_id(created_test_user.id)
        assert db_helper.user_exists_by_email("api1@gmail.com")

    def test_db_create_and_delete_movie(self, super_admin, db_helper, db_session):
        movie_name = f"{DataGenerator.generate_movie_name()}"

        # Тестовый фильм
        test_movie = TestMovie(
            name=movie_name,
            imageUrl=DataGenerator.generate_image_url(),
            price=DataGenerator.generate_movie_price(),
            description=DataGenerator.generate_movie_description(),
            location=DataGenerator.generate_movie_location(),
            published=DataGenerator.generate_movie_is_published(),
            genreId=DataGenerator.generate_genreId()
        )

        # Проверки отсутствия фильма в базе данных
        movies_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.name == movie_name)
        assert movies_from_db.count() == 0, f"Число записей в таблице movies != 0"
        assert db_helper.get_movie_by_name(movie_name) is None, f"Фильм с {movie_name} есть в базе"

        # Создание фильма
        response = super_admin.api.movie_api.create_movie(test_movie)
        response_create_movie = MovieCreatedResponse(**response.json())
        movie_id = response_create_movie.id

        movie_db_exist = db_helper.movie_exist_by_name(movie_name)
        movie_db_name = db_helper.get_movie_by_name(movie_name).name
        movie_db_id = db_helper.get_movie_by_name(movie_name).id

        # Проверка данных фильма в бд
        assert movie_db_exist == True, "Фильма нет в базе данных"
        assert movie_db_name == movie_name, "имя фильма в базе отличается от тестового имени фильма"
        assert movie_db_id == movie_id, "Id фильма в базе отличается от тестового Id фильма"

        # Удаление фильма
        delete_movie = response_create_movie
        super_admin.api.movie_api.delete_movie_by_id(delete_movie)

        # Проверка отсутствия фильма в бд
        assert movies_from_db.count() == 0, f"Число записей в таблице movies != 0"
        assert db_helper.get_movie_by_name(movie_name) is None, f"Фильм с {movie_name} есть в базе"






