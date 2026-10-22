"""API класс для работы с Movies."""

from typing import Optional, Dict, Any
from api.base_api import BaseAPI
from http import HTTPStatus


class MoviesAPI(BaseAPI):
    """API-класс для работы с эндпоинтами /movies."""

    def get_movies(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        GET /movies - Получение афиш фильмов.
        """
        response = self.requester.send_request(
            "GET",
            "movies",  # Без слэша
            params=params,
            expected_status=HTTPStatus.OK
        )
        return response.json()

    def create_movie(self, data: Dict[str, Any], expected_status=HTTPStatus.CREATED) -> Dict[str, Any]:
        """
        POST /movies - Создание фильма.
        """
        response = self.requester.send_request(
            "POST",
            "movies",  # Без слэша
            data=data,
            expected_status=expected_status
        )
        return response.json()

    def get_movie_by_id(self, movie_id: int) -> Dict[str, Any]:
        """
        GET /movies/{id} - Получение фильма по ID.
        """
        response = self.requester.send_request(
            "GET",
            f"movies/{movie_id}",  # Без слэша
            expected_status=HTTPStatus.OK
        )
        return response.json()

    def delete_movie(self, movie_id: int, expected_status: int = HTTPStatus.OK) -> Dict[str, Any]:

        response = self.requester.send_request(
            "DELETE",
            f"movies/{movie_id}",
            expected_status=expected_status
        )
        return response.json()

    def patch_movie(self, movie_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        PATCH /movies/{id} - Редактирование фильма.
        """
        response = self.requester.send_request(
            "PATCH",
            f"movies/{movie_id}",  # Без слэша
            data=data,
            expected_status=HTTPStatus.OK
        )
        return response.json()