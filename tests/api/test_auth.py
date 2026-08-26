import pytest
import allure
import datetime
from constants.roles import Roles
from pytest_check import check
from clients.api_manager import ApiManager
from models.base_models import TestUser
from conftest import api_manager, test_user
from models.base_models import RegisterUserResponse, LoginUserResponse
from resources.user_creds import SuperAdminCreds


class TestAuth:

    def test_register_user(self, api_manager: ApiManager, test_user):
        response = api_manager.auth_api.register_user(test_user)
        register_user_response = RegisterUserResponse(**response.json())

        assert register_user_response.email == test_user.email, "Email не совпадает"


    def test_login_user(self, api_manager: ApiManager, registered_user):
        user, password = registered_user
        login_data = {
            "email": user.email,
            "password": password
        }

        response = api_manager.auth_api.login_user(login_data)
        login_user_response = LoginUserResponse(**response.json())

        assert login_user_response.user.email == user.email
        assert login_user_response.user.fullName == user.fullName
        assert login_user_response.user.roles == user.roles

        api_manager.auth_api.authenticate((login_data["email"], login_data["password"]))


    def test_logout_user(self, api_manager):
        response = api_manager.auth_api.logout_user()
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    @pytest.mark.parametrize(
        "email,password,expected_status",
        [
            (f"{SuperAdminCreds.USERNAME}", f"{SuperAdminCreds.PASSWORD}", (200, 201)),
            ("test_login1@email.com", "asdqwe123Q!", (401,)),
            ("", "password", (401,))
        ],
        ids=["Admin login", "Invalid user", "Empty username"]
    )
    def test_login(self, email, password, expected_status, api_manager):
        login_data = {
            "email": email,
            "password": password
        }
        api_manager.auth_api.login_user(login_data=login_data, expected_status=expected_status)


    @allure.title("Тест регистрации пользователя с помощью Mock")
    @allure.severity(allure.severity_level.MINOR)
    @allure.label("qa_name", "Ivan Petrovich")
    @pytest.mark.skip
    def test_register_user_mock(self, api_manager: ApiManager, test_user: TestUser, mocker):
        with allure.step(" Мокаем метод register_user в auth_api"):
            mock_response = RegisterUserResponse(  # Фиктивный ответ
                id="id",
                email="email@email.com",
                fullName="fullName",
                verified=True,
                banned=False,
                roles=[Roles.SUPER_ADMIN],
                createdAt=str(datetime.datetime.now())
            )

            mocker.patch.object(
                api_manager.auth_api,  # Объект, который нужно замокать
                'register_user',  # Метод, который нужно замокать
                return_value=mock_response  # Фиктивный ответ
            )

        with allure.step("Вызываем метод, который должен быть замокан"):
            register_user_response = api_manager.auth_api.register_user(test_user)

        with allure.step("Проверяем, что ответ соответствует ожидаемому"):
            with allure.step("Проверка поля персональных данных"):  # обратите внимание на вложенность allure.step
                with check:
                    # Строка ниже выдаст исключение, но выполнение теста продолжится
                    check.equal(register_user_response.fullName, "INCORRECT_NAME", "НЕСОВПАДЕНИЕ fullName")
                    check.equal(register_user_response.email, mock_response.email)

            with allure.step("Проверка поля banned"):
                with check("Проверка поля banned"):  # можно использовать вместо allure.step
                    check.equal(register_user_response.banned, mock_response.banned)



"""

    def test_get_user_me(self, api_manager, registered_user):
        api_manager.auth_api.authenticate((registered_user["email"], registered_user["password"]))
        response = api_manager.user_api.get_user_info()
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"


    def test_get_user_info(self, api_manager, authenticated_user):
        response = api_manager.user_api.get_user_info()
        response_data = response.json()

        assert "email" in response_data
        assert "id" in response_data

    def test_register_and_delete_three_users(self, api_manager, test_user, prefix_email):
        users_count = 0
        list_users = []
        list_users_ids = []
        while users_count < 3:
            
            Генерация уникальной почты (так как будет ошибка при попытке 
            повторно зарегать юзера с теми же данными)
            
            test_user["email"] = str(prefix_email) + test_user["email"]
            response = api_manager.auth_api.register_user(test_user)
            response_data = response.json()

            list_users_ids.append(response_data["id"])
            list_users.append(response_data)

            users_count += 1

        
        Делаем аутентификацию под админскими кредами, 
        так как удаление под правами админа или суперадмина
        
        api_manager.auth_api.authenticate(("api1@gmail.com", "asdqwe123Q"))

        # Передаем список id на удаление
        api_manager.user_api.delete_users(*list_users_ids)

        # Проверяем в цикле, что данных нет (для себя)
        for user_id in list_users_ids:
            api_manager.user_api.get_user_info_by_id(user_id)

"""