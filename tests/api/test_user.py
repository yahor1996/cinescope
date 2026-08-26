from models.base_models import RegisterUserResponse, ErrorResponse


class TestUser:

    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data)
        create_user_response = RegisterUserResponse(**response.json())

        assert create_user_response.id != "", "ID должен быть не пустым"
        assert create_user_response.email == creation_user_data.email
        assert create_user_response.fullName == creation_user_data.fullName
        assert create_user_response.roles == creation_user_data.roles
        assert create_user_response.verified is True


    def test_get_user_by_locator(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data)
        created_user_response = RegisterUserResponse(**response.json())

        response_by_id = super_admin.api.user_api.get_user(created_user_response.id)
        response_user_by_id = RegisterUserResponse(**response_by_id.json())

        response_by_email = super_admin.api.user_api.get_user(creation_user_data.email)
        response_user_by_email = RegisterUserResponse(**response_by_email.json())

        assert response_user_by_id == response_user_by_email, "Содержание ответов должно быть идентичным"
        assert response_user_by_id.id != '', "ID должен быть не пустым"
        assert response_user_by_id.email == creation_user_data.email
        assert response_user_by_id.fullName == creation_user_data.fullName
        assert response_user_by_id.roles == creation_user_data.roles
        assert response_user_by_id.verified is True


    def test_get_user_by_id_common_user(self, common_user):
        response = common_user.api.user_api.get_user(common_user.email, expected_status=(403,))
        error_response = ErrorResponse(**response.json())

        assert error_response.message == "Forbidden resource"
        assert error_response.error == "Forbidden"
        assert error_response.statusCode == 403
