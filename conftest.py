import time
import pytest
import requests
from utils.data_generator import DataGenerator
from clients.api_manager import ApiManager
from resources.user_creds import SuperAdminCreds
from entities.user import User
from constants.roles import Roles
from models.base_models import TestUser, RegisterUserResponse
from models.movie_models import TestMovie, MovieCreatedResponse
from sqlalchemy.orm import Session
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper


@pytest.fixture(scope="class")
def api_manager(session):
    return ApiManager(session)


@pytest.fixture(scope="class")
def session():
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture
def test_user() -> TestUser:
    password = DataGenerator.generate_valid_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=f"{DataGenerator.generate_firstname()} {DataGenerator.generate_lastname()}",
        password=password,
        passwordRepeat=password,
        roles=[Roles.USER.value]
    )


@pytest.fixture
def creation_user_data(test_user) -> TestUser:
    updated_data = test_user.model_copy(update={
        "verified": True,
        "banned": False,
    })
    return updated_data


@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.USER.value],
        new_session
    )

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture
def admin(user_session, super_admin, creation_user_data):
    new_session = user_session()

    admin = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.ADMIN.value],
        new_session
    )

    response_data = super_admin.api.user_api.create_user(creation_user_data).json()
    admin_data = response_data.copy()
    admin_id = response_data["id"]
    admin_data["roles"].append(Roles.ADMIN.value)

    super_admin.api.user_api.patch_user(admin_id, admin_data)
    admin.api.auth_api.authenticate(admin.creds)
    return admin


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


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session
    )

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture(scope="function")
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user)
    registered_user = RegisterUserResponse(**response.json())
    password = test_user.password
    return registered_user, password


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
def test_movie() -> TestMovie:
    return TestMovie(
        name=DataGenerator.generate_movie_name(),
        imageUrl=DataGenerator.generate_image_url(),
        price=DataGenerator.generate_movie_price(),
        description=DataGenerator.generate_movie_description(),
        location=DataGenerator.generate_movie_location(),
        published=DataGenerator.generate_movie_is_published(),
        genreId=DataGenerator.generate_genreId()
    )


@pytest.fixture
def created_movie(api_manager, test_movie):
    api_manager.auth_api.authenticate((SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD))
    response = api_manager.movie_api.create_movie(test_movie)
    response_created_movie = MovieCreatedResponse(**response.json())
    return response_created_movie


@pytest.fixture
def patch_movie_data():
    return {
        "name": DataGenerator.generate_movie_name(),
        "price": DataGenerator.generate_movie_price()
    }


@pytest.fixture
def params_movie(created_movie):
    return {
        "genreId": created_movie.genreId,
        "location": created_movie.location,
        "minPrice": created_movie.price
    }

@pytest.fixture
def fake_movie_id():
    return DataGenerator.generate_wrong_movie_id()

@pytest.fixture
def prefix_email():
    return DataGenerator.generate_prefix_email()

@pytest.fixture
def registration_user_data():
    random_password = DataGenerator.generate_valid_password()

    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": f"{DataGenerator.generate_firstname()} {DataGenerator.generate_lastname()}",
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value]
    }


@pytest.fixture(scope="module")
def db_session() -> Session:
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных
    После завершения теста сессия автоматически закрывается
    """
    db_session = get_db_session()
    yield db_session
    db_session.close()


@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    """
    Фикстура для экземпляра хелпера
    """
    db_helper = DBHelper(db_session)
    return db_helper


@pytest.fixture(scope="function")
def created_test_user(db_helper):
    """
    Фикстура, которая создает тестового пользователя в БД
    и удаляет его после завершения теста
    """
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    # Cleanup после теста
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)


@pytest.fixture
def delay_between_retries():
    time.sleep(2)  # Задержка в 2 секунды\ это не обязательно но
    yield          # нужно понимать что такая возможность имеется









