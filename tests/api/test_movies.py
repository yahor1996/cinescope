import pytest
import allure
from conftest import common_user, admin, super_admin
from models.movie_models import GetMoviesResponse, MovieCreatedResponse
from models.base_models import ErrorResponse


@allure.epic("Тестирование api для работы с фильмами. Позитив.")
class TestMovies:

    @pytest.mark.api
    @pytest.mark.smoke
    @allure.title("Тест. Получение списка фильмов по дефолту.")
    # created_movie на случай если фильмов нет никаких
    def test_get_movies(self, common_user, created_movie):
        response = common_user.api.movie_api.get_movies()
        response_get_movies = GetMoviesResponse(**response.json())

        assert len(response_get_movies.movies) > 0, "Список фильмов пуст"
        assert response_get_movies.movies[0].id != "", "ID фильма должен быть не пустым"
        assert response_get_movies.movies[0].name != "", "Имя фильма должно быть не пустое"


    @pytest.mark.api
    @pytest.mark.regression
    @allure.title("Тест. Получение списка фильмов по фильтрам.")
    def test_get_movies_with_params(self, common_user, params_movie):
        response = common_user.api.movie_api.get_movies(
            params=params_movie
        )
        response_get_movies = GetMoviesResponse(**response.json())

        assert len(response_get_movies.movies) > 0, "Список фильмов пуст"


    @pytest.mark.parametrize(
        "price,locations,genre_id",
        [([1, 1000], ["MSK", "SPB"], 5)],
        ids=["price_range_and_multi_locations"]
    )
    @pytest.mark.api
    @pytest.mark.regression
    @allure.title("Тест. Получение списка фильмов. Параметризованный тест с @parametrize.")
    def test_get_movies_parametrize(self, price, locations, genre_id, common_user):
        response = common_user.api.movie_api.get_movies(
            params={
                "minPrice": price[0],
                "maxPrice": price[1],
                "locations": locations,
                "genreId": genre_id
            }
        )
        response_get_movies = GetMoviesResponse(**response.json())

        assert len(response_get_movies.movies) > 0, "Список фильмов пуст"


    @pytest.mark.api
    @pytest.mark.smoke
    @allure.title("Тест. Создание фильма.")
    def test_create_movie(self, super_admin, test_movie):
        response = super_admin.api.movie_api.create_movie(test_movie)
        response_create_movie = MovieCreatedResponse(**response.json())

        assert response_create_movie.id != "", "ID фильма должен быть не пустым"
        assert response_create_movie.name == test_movie.name


    @pytest.mark.api
    @pytest.mark.smoke
    @allure.title("Тест. Получение фильма по id.")
    def test_get_movie_by_id(self, common_user, created_movie):
        response = common_user.api.movie_api.get_movie_by_id(created_movie)
        response_get_movie = MovieCreatedResponse(**response.json())

        assert response_get_movie.id == created_movie.id, f"{response_get_movie.id != created_movie.id}"
        assert response_get_movie.name == created_movie.name, f"{response_get_movie.name != created_movie.name}"


    @pytest.mark.api
    @pytest.mark.smoke
    @allure.title("Тест. Удаление фильма по id.")
    def test_delete_movie_by_id(self, super_admin, created_movie):
        # Проверяем что есть фильм
        response = super_admin.api.movie_api.get_movie_by_id(created_movie)
        response_get_movie = MovieCreatedResponse(**response.json())

        assert response_get_movie.id == created_movie.id

        # Удаляем фильм
        response = super_admin.api.movie_api.delete_movie_by_id(created_movie)
        response_delete_movie = MovieCreatedResponse(**response.json())

        assert response_delete_movie.id == created_movie.id

        # Проверяем что фильма уже нет
        response = super_admin.api.movie_api.get_movie_by_id(created_movie, expected_status=(404,))
        error_response = ErrorResponse(**response.json())

        assert error_response.message == "Фильм не найден"
        assert error_response.error == "Not Found"
        assert error_response.statusCode == 404


    @pytest.mark.parametrize(
        "user_name,expected_deleted_status,expected_get_status",
        [
            ("common_user", (403,), (200,)),
            ("admin", (403,), (200,)),
            ("super_admin", (200,), (404,))
        ],
        ids=["user", "admin", "super_admin"]
    )
    @pytest.mark.api
    @pytest.mark.regression
    @allure.title("Тест. Удаление фильма по id. Параметризованный тест с @parametrize.")
    def test_delete_movie_parametrize(
            self,
            request,
            user_name,
            expected_deleted_status,
            expected_get_status,
            super_admin,
            created_movie
    ):

        # Преобразуем стрингу в юзера
        user = request.getfixturevalue(user_name)

        # Проверяем что есть фильм
        response = super_admin.api.movie_api.get_movie_by_id(created_movie)
        response_get_movie = MovieCreatedResponse(**response.json())
        assert response_get_movie.id == created_movie.id

        # Удаляем фильм
        response = user.api.movie_api.delete_movie_by_id(
            created_movie,
            expected_status=expected_deleted_status
        )

        # Проверка ответа через модели
        try:
            response_delete_movie = MovieCreatedResponse(**response.json())
            assert response_delete_movie.id == created_movie.id
        except Exception as e:
            error_response = ErrorResponse(**response.json())
            assert error_response.message == "Forbidden resource"
            assert error_response.error == "Forbidden"
            assert error_response.statusCode == 403

        # Проверяем сработало ли удаление в зависимости от роли
        user.api.movie_api.get_movie_by_id(created_movie, expected_status=expected_get_status)

    @pytest.mark.api
    @pytest.mark.smoke
    @allure.title("Тест. Обновление данных фильма.")
    def test_patch_movie_by_id(self, super_admin, created_movie, patch_movie_data):
        # Проверяем что есть фильм
        response = super_admin.api.movie_api.get_movie_by_id(created_movie)
        response_get_movie = MovieCreatedResponse(**response.json())

        assert response_get_movie.id == created_movie.id

        # Обновляем фильм
        response = super_admin.api.movie_api.patch_movie_by_id(
            movie=created_movie,
            data_update=patch_movie_data
        )
        response_patch_movie = MovieCreatedResponse(**response.json())

        assert response_patch_movie.name != created_movie.name, f"name not changed"
        assert response_patch_movie.price != created_movie.price, f"price not changed"


@allure.epic("Тестирование api для работы с фильмами. Негатив.")
class TestMoviesNegative:

    @pytest.mark.api
    @pytest.mark.regression
    @allure.title("Негативный тест. Получение фильмов по невалидному фильтру.")
    def test_get_movies_negative(self, common_user):
       response = common_user.api.movie_api.get_movies(
           params={
               "pageSize": "qwerty"
           },
           expected_status=(400,)
       )
       error_response = ErrorResponse(**response.json())

       assert error_response.message != ""
       assert error_response.error == "Bad Request"
       assert error_response.statusCode == 400


    @pytest.mark.api
    @pytest.mark.regression
    @allure.title("Негативный тест. Создание фильма.")
    def test_create_movie_negative(self, common_user, test_movie):
        response = common_user.api.movie_api.create_movie(
            test_movie=test_movie,
            expected_status=(403,)
        )
        error_response = ErrorResponse(**response.json())

        assert error_response.message == "Forbidden resource"
        assert error_response.error == "Forbidden"
        assert error_response.statusCode == 403


    @pytest.mark.api
    @pytest.mark.regression
    @allure.title("Негативный тест. Получение фильма по id.")
    def test_get_movie_by_id_negative(self, common_user, created_movie, fake_movie_id):
        created_wrong_movie = created_movie.copy()
        created_wrong_movie.id = fake_movie_id

        response = common_user.api.movie_api.get_movie_by_id(
            movie=created_wrong_movie,
            expected_status=(404,)
        )
        error_response = ErrorResponse(**response.json())

        assert error_response.message == "Фильм не найден"
        assert error_response.error == "Not Found"
        assert error_response.statusCode == 404


    @pytest.mark.api
    @pytest.mark.regression
    @allure.title("Негативный тест. Удаление фильма.")
    def test_delete_movie_by_id_negative(self, super_admin, created_movie, fake_movie_id):
        #Создаем фильм с невалидным айди
        created_wrong_movie = created_movie
        created_wrong_movie.id = fake_movie_id

        # Пытаемся удалить фильм с невалидным айди
        response = super_admin.api.movie_api.delete_movie_by_id(
            movie=created_wrong_movie,
            expected_status=(404,)
        )
        error_response = ErrorResponse(**response.json())

        assert error_response.message == "Фильм не найден"
        assert error_response.error == "Not Found"
        assert error_response.statusCode == 404


    @pytest.mark.api
    @pytest.mark.regression
    @allure.title("Негативный тест. Обновление данных фильма.")
    def test_patch_movie_by_id_negative(self, super_admin, created_movie, patch_movie_data, fake_movie_id):
        # Проверяем что есть фильм
        response = super_admin.api.movie_api.get_movie_by_id(created_movie)
        response_get_movie = MovieCreatedResponse(**response.json())

        assert response_get_movie.id == created_movie.id

        # Обновляем фильм
        patch_movie_data["review"] = "bad"
        response = super_admin.api.movie_api.patch_movie_by_id(
            movie=created_movie,
            data_update=patch_movie_data,
            expected_status=(404,)
        )
        error_response = ErrorResponse(**response.json())

        assert error_response.message == "Фильм не найден"
        assert error_response.error == "Not Found"
        assert error_response.statusCode == 404
