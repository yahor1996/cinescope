import pytest
import requests
from utils.data_generator import DataGenerator
from clients.api_manager import ApiManager
from resources.user_creds import SuperAdminCreds


@pytest.fixture(scope="class")
def api_manager(session):
    return ApiManager(session)


@pytest.fixture(scope="class")
def session():
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture
def test_user(roles=None):
    password = DataGenerator.generate_valid_password()
    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": f"{DataGenerator.generate_firstname()} {DataGenerator.generate_lastname()}",
        "password": password,
        "passwordRepeat": password,
        "roles": roles or ["USER"]
    }

@pytest.fixture
def test_movie():
    return {
        "name": DataGenerator.generate_movie_name(),
        "imageUrl": DataGenerator.generate_image_url(),
        "price": DataGenerator.generate_movie_price(),
        "description": DataGenerator.generate_movie_description(),
        "location": DataGenerator.generate_movie_location(),
        "published": DataGenerator.generate_movie_is_published(),
        "genreId": DataGenerator.generate_genreId()
    }

@pytest.fixture
def created_movie(api_manager, test_movie):
    api_manager.auth_api.authenticate((SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD))
    response = api_manager.movie_api.create_movie(test_movie)
    response_data = response.json()
    return response_data

@pytest.fixture
def patch_movie_data():
    return {
        "name": DataGenerator.generate_movie_name(),
        "price": DataGenerator.generate_movie_price()
    }

@pytest.fixture(scope="function")
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user).json()
    test_user["id"] = response["id"]
    return test_user


@pytest.fixture(scope="session")
def unauthenticated_api_manager(registered_user):
    session = requests.Session()
    yield ApiManager(session)
    session.close()


@pytest.fixture(scope="function")
def authenticated_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user)
    response_data = response.json()
    api_manager.auth_api.authenticate((test_user["email"], test_user["password"]))
    return response_data

@pytest.fixture
def params_movie(created_movie):
    return {
        "genreId": created_movie["genreId"],
        "location": created_movie["location"],
        "minPrice": created_movie["price"]
    }

@pytest.fixture
def fake_movie_id():
    return DataGenerator.generate_wrong_movie_id()

@pytest.fixture
def prefix_email():
    return DataGenerator.generate_prefix_email()

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()