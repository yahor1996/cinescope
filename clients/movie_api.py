from custom_requester.custom_requester import CustomRequester
from config.base_urls import MOVIES_BASE_URL

MOVIES ="/movies"


class MovieApi(CustomRequester):

    def __init__(self, session):
        super().__init__(session=session, base_url=MOVIES_BASE_URL)

    def get_movies(self, expected_status=200, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=MOVIES,
            expected_status=expected_status,
            **kwargs
        )

    def create_movie(self, test_movie, expected_status=201, **kwargs):
        return self.send_request(
            method="POST",
            endpoint=MOVIES,
            data=test_movie,
            expected_status=expected_status,
            **kwargs
        )

    def get_movie_by_id(self, movie, expected_status=200, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES}/{movie["id"]}",
            expected_status=expected_status,
            **kwargs
        )

    def delete_movie_by_id(self, movie, expected_status=200, **kwargs):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES}/{movie["id"]}",
            expected_status=expected_status,
            **kwargs
        )

    def patch_movie_by_id(self, movie, data_update, expected_status=200, **kwargs):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES}/{movie["id"]}",
            data=data_update,
            expected_status=expected_status,
            **kwargs
        )