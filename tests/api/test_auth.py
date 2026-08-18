import pytest
from conftest import api_manager, test_user
from resources.user_creds import SuperAdminCreds


class TestAuth:

    def test_register_user(self, api_manager, test_user):
        response = api_manager.auth_api.register_user(test_user, timeout=5, verify=False)
        response_data = response.json()

        assert response_data["email"] == test_user["email"]
        assert "id" in response_data
        assert "USER" in response_data["roles"]


    def test_login_user(self, api_manager, registered_user):
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }

        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        assert "accessToken" in response_data
        assert response_data["user"]["email"] == registered_user["email"]

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