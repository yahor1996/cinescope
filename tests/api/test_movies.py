from conftest import api_manager
from config.credentials import ADMIN_USERNAME, ADMIN_PASSWORD


class TestMovies:

    # created_movie на случай если фильмов нет никаких
    def test_get_movies(self, api_manager, created_movie):
        response = api_manager.movie_api.get_movies()

        assert response.status_code == 200, f"Status code: {response.status_code}"

    def test_get_movies_with_params(self, api_manager, params_movie):
        response = api_manager.movie_api.get_movies(
            params=params_movie
        )
        response_data = response.json()

        assert response.status_code == 200, f"Status code: {response.status_code}"
        assert "movies" in response_data
        assert len(response_data["movies"]) >= 1, f"Movies count: {len(response_data["movies"])}"

    def test_create_movie(self, api_manager, test_movie):
        api_manager.auth_api.authenticate((ADMIN_USERNAME, ADMIN_PASSWORD))
        response = api_manager.movie_api.create_movie(test_movie)
        response_data = response.json()

        assert response.status_code == 201, f"Status code: {response.status_code}"
        assert "id" in response_data
        assert response_data["name"] == test_movie["name"]

    def test_get_movie_by_id(self, api_manager, created_movie):
        response = api_manager.movie_api.get_movie_by_id(created_movie)
        response_data = response.json()

        assert response.status_code == 200, f"Status code: {response.status_code}"
        assert response_data["id"] == created_movie["id"], f"{response_data["id"] != {created_movie["id"]}}"
        assert response_data["name"] == created_movie["name"], f"{response_data["name"] != {created_movie["name"]}}"

    def test_delete_movie_by_id(self, api_manager, created_movie):
        # Проверяем что есть фильм
        response = api_manager.movie_api.get_movie_by_id(created_movie)
        response_data = response.json()

        assert response_data["id"] == created_movie["id"]

        # Удаляем фильм
        response = api_manager.movie_api.delete_movie_by_id(created_movie)
        response_data = response.json()

        assert response_data["id"] == created_movie["id"]

        # Проверяем что фильма уже нет
        response = api_manager.movie_api.get_movie_by_id(created_movie, expected_status=404)
        response_data = response.json()

        assert response_data["message"] == "Фильм не найден"
        assert response_data["error"] == "Not Found"
        assert response_data["statusCode"] == 404

    def test_patch_movie_by_id(self, api_manager, created_movie, patch_movie_data):
        # Проверяем что есть фильм
        response = api_manager.movie_api.get_movie_by_id(created_movie)
        response_data = response.json()

        assert response_data["id"] == created_movie["id"]

        # Обновляем фильм
        response = api_manager.movie_api.patch_movie_by_id(
            movie=created_movie,
            data_update=patch_movie_data
        )
        response_data = response.json()

        assert response_data["name"] != created_movie["name"], f"name not changed"
        assert response_data["price"] != created_movie["price"], f"name not changed"


class TestMoviesNegative:

    def test_get_movies_negative(self, api_manager):
       response = api_manager.movie_api.get_movies(
           params={
               "pageSize": "qwerty"
           },
           expected_status=400
       )
       response_data = response.json()

       assert "message" in response_data
       assert response_data["error"] == "Bad Request"
       assert response_data["statusCode"] == 400

    def test_create_movie_negative(self, api_manager, test_movie):
        response = api_manager.movie_api.create_movie(
            test_movie=test_movie,
            expected_status=401
        )
        response_data = response.json()

        assert "message" in response_data
        assert response_data["message"] == "Unauthorized"
        assert response_data["statusCode"] == 401

    def test_get_movie_by_id_negative(self, api_manager, created_movie, fake_movie_id):
        created_wrong_movie = created_movie
        created_wrong_movie["id"] = fake_movie_id

        response = api_manager.movie_api.get_movie_by_id(
            movie=created_wrong_movie,
            expected_status=404
        )
        response_data = response.json()

        assert "message" in response_data
        assert response_data["message"] == "Фильм не найден"
        assert response_data["error"] == "Not Found"
        assert response_data["statusCode"] == 404

    def test_delete_movie_by_id_negative(self, api_manager, created_movie, fake_movie_id):
        #Создаем фильм с невалидным айди
        created_wrong_movie = created_movie
        created_wrong_movie["id"] = fake_movie_id

        # Пытаемся удалить фильм с невалидным айди
        response = api_manager.movie_api.delete_movie_by_id(
            movie=created_wrong_movie,
            expected_status=404
        )
        response_data = response.json()

        assert "message" in response_data
        assert response_data["message"] == "Фильм не найден"
        assert response_data["error"] == "Not Found"
        assert response_data["statusCode"] == 404

    def test_patch_movie_by_id_negative(self, api_manager, created_movie, patch_movie_data, fake_movie_id):
        # Проверяем что есть фильм
        response = api_manager.movie_api.get_movie_by_id(created_movie)
        response_data = response.json()

        assert response_data["id"] == created_movie["id"]

        # Обновляем фильм
        patch_movie_data["review"] = "bad"
        response = api_manager.movie_api.patch_movie_by_id(
            movie=created_movie,
            data_update=patch_movie_data,
            expected_status=404
        )
        response_data = response.json()
        
        assert "message" in response_data
        assert response_data["message"] == "Фильм не найден"
        assert response_data["error"] == "Not Found"
        assert response_data["statusCode"] == 404
