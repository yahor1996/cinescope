import pytest


class TestMovies:

    # created_movie на случай если фильмов нет никаких
    def test_get_movies(self, common_user, created_movie):
        response = common_user.api.movie_api.get_movies()

    def test_get_movies_with_params(self, common_user, params_movie):
        response = common_user.api.movie_api.get_movies(
            params=params_movie
        )
        response_data = response.json()

        assert "movies" in response_data
        assert len(response_data["movies"]) >= 1, f"Movies count: {len(response_data["movies"])}"

    @pytest.mark.parametrize(
        "price,locations,genre_id",
        [([1, 1000], ["MSK", "SPB"], 1)],
        ids=["price_range_and_multi_locations"]
    )
    def test_get_movies_parametrize(self, price, locations, genre_id, common_user):
        response = common_user.api.movie_api.get_movies(
            params={
                "minPrice": price[0],
                "maxPrice": price[1],
                "locations": locations,
                "genreId": genre_id
            }
        )
        response_data = response.json()

        assert "movies" in response_data
        assert len(response_data["movies"]) >= 1, f"Movies count: {len(response_data["movies"])}"

    def test_create_movie(self, super_admin, test_movie):
        response = super_admin.api.movie_api.create_movie(test_movie)
        response_data = response.json()

        assert "id" in response_data
        assert response_data["name"] == test_movie["name"]

    def test_get_movie_by_id(self, common_user, created_movie):
        response = common_user.api.movie_api.get_movie_by_id(created_movie)
        response_data = response.json()

        assert response_data["id"] == created_movie["id"], f"{response_data["id"] != {created_movie["id"]}}"
        assert response_data["name"] == created_movie["name"], f"{response_data["name"] != {created_movie["name"]}}"

    def test_delete_movie_by_id(self, super_admin, created_movie):
        # Проверяем что есть фильм
        response = super_admin.api.movie_api.get_movie_by_id(created_movie)
        response_data = response.json()

        assert response_data["id"] == created_movie["id"]

        # Удаляем фильм
        response = super_admin.api.movie_api.delete_movie_by_id(created_movie)
        response_data = response.json()

        assert response_data["id"] == created_movie["id"]

        # Проверяем что фильма уже нет
        response = super_admin.api.movie_api.get_movie_by_id(created_movie, expected_status=(404,))
        response_data = response.json()

        assert response_data["message"] == "Фильм не найден"
        assert response_data["error"] == "Not Found"
        assert response_data["statusCode"] == 404

    def test_patch_movie_by_id(self, super_admin, created_movie, patch_movie_data):
        # Проверяем что есть фильм
        response = super_admin.api.movie_api.get_movie_by_id(created_movie)
        response_data = response.json()

        assert response_data["id"] == created_movie["id"]

        # Обновляем фильм
        response = super_admin.api.movie_api.patch_movie_by_id(
            movie=created_movie,
            data_update=patch_movie_data
        )
        response_data = response.json()

        assert response_data["name"] != created_movie["name"], f"name not changed"
        assert response_data["price"] != created_movie["price"], f"name not changed"


class TestMoviesNegative:

    def test_get_movies_negative(self, common_user):
       response = common_user.api.movie_api.get_movies(
           params={
               "pageSize": "qwerty"
           },
           expected_status=(400,)
       )
       response_data = response.json()

       assert "message" in response_data
       assert response_data["error"] == "Bad Request"
       assert response_data["statusCode"] == 400

    def test_create_movie_negative(self, common_user, test_movie):
        response = common_user.api.movie_api.create_movie(
            test_movie=test_movie,
            expected_status=(403,)
        )
        response_data = response.json()

        assert "message" in response_data
        assert response_data["message"] == "Forbidden resource"
        assert response_data["error"] == "Forbidden"
        assert response_data["statusCode"] == 403

    def test_get_movie_by_id_negative(self, common_user, created_movie, fake_movie_id):
        created_wrong_movie = created_movie.copy()
        created_wrong_movie["id"] = fake_movie_id

        response = common_user.api.movie_api.get_movie_by_id(
            movie=created_wrong_movie,
            expected_status=(404,)
        )
        response_data = response.json()

        assert "message" in response_data
        assert response_data["message"] == "Фильм не найден"
        assert response_data["error"] == "Not Found"
        assert response_data["statusCode"] == 404

    def test_delete_movie_by_id_negative(self, super_admin, created_movie, fake_movie_id):
        #Создаем фильм с невалидным айди
        created_wrong_movie = created_movie
        created_wrong_movie["id"] = fake_movie_id

        # Пытаемся удалить фильм с невалидным айди
        response = super_admin.api.movie_api.delete_movie_by_id(
            movie=created_wrong_movie,
            expected_status=(404,)
        )
        response_data = response.json()

        assert "message" in response_data
        assert response_data["message"] == "Фильм не найден"
        assert response_data["error"] == "Not Found"
        assert response_data["statusCode"] == 404

    def test_patch_movie_by_id_negative(self, super_admin, created_movie, patch_movie_data, fake_movie_id):
        # Проверяем что есть фильм
        response = super_admin.api.movie_api.get_movie_by_id(created_movie)
        response_data = response.json()

        assert response_data["id"] == created_movie["id"]

        # Обновляем фильм
        patch_movie_data["review"] = "bad"
        response = super_admin.api.movie_api.patch_movie_by_id(
            movie=created_movie,
            data_update=patch_movie_data,
            expected_status=(404,)
        )
        response_data = response.json()
        
        assert "message" in response_data
        assert response_data["message"] == "Фильм не найден"
        assert response_data["error"] == "Not Found"
        assert response_data["statusCode"] == 404
