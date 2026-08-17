"""
from custom_requester.custom_requester import CustomRequester
from config.base_urls import AUTH_BASE_URL

USER ="/user"


class UserApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=AUTH_BASE_URL)

    def get_user_info(self, expected_status=200, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=f"{USER}/me",
            expected_status=expected_status,
            **kwargs
        )

    def get_user_info_by_id(self, user_id, expected_status=200, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=f"{USER}/{user_id}",
            expected_status=expected_status,
            **kwargs
        )

    def delete_user(self, user_id, expected_status=200, **kwargs):
        return self.send_request(
            method="DELETE",
            endpoint=f"{USER}/{user_id}",
            expected_status=expected_status,
            **kwargs
        )

    def delete_users(self, *user_ids, **kwargs):
        for user_id in user_ids:
            self.delete_user(user_id, **kwargs)
"""


from custom_requester.custom_requester import CustomRequester


class UserApi(CustomRequester):
    USER_BASE_URL = "https://auth.dev-cinescope.coconutqa.ru/"

    def __init__(self, session):
        self.session = session
        super().__init__(session, base_url=self.USER_BASE_URL)

    def get_user(self, user_locator, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=f"user/{user_locator}",
            expected_status=expected_status
        )

    def create_user(self, user_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint="user",
            data=user_data,
            expected_status=expected_status
        )

    def patch_user(self, user_id, user_data, expected_status=200):
        return self.send_request(
            method="PATCH",
            endpoint=f"user/{user_id}",
            data=user_data,
            expected_status=expected_status
        )






