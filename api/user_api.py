"""API класс для работы с пользователями."""

from typing import Dict, Any, Optional
from api.base_api import BaseAPI
from http import HTTPStatus
from core.custom_requester import CustomRequester


class UserAPI:
    """
    API-класс для работы с пользователями.
    Базовый URL: https://auth.dev-cinescope.coconutqa.ru/
    """

    def __init__(self, requester):
        """
        Инициализация UserAPI.
        """
        self.requester = requester
        self.user_base_url = "https://auth.dev-cinescope.coconutqa.ru/"

    def create_user(self, user_data: Dict[str, Any], expected_status: int = HTTPStatus.CREATED):
        """
        POST /user - Создание нового пользователя.
        Возвращает response (НЕ response.json()).
        """
        return self.requester.send_request(
            method="POST",
            endpoint="user",
            data=user_data,
            expected_status=expected_status,
            base_url=self.user_base_url
        )

    def get_user(self, user_locator: str, expected_status: int = HTTPStatus.OK):
        """
        GET /user/{id} или /user/{email} - Получение пользователя.
        Возвращает response (НЕ response.json()).
        """
        return self.requester.send_request(
            method="GET",
            endpoint=f"user/{user_locator}",
            expected_status=expected_status,
            base_url=self.user_base_url
        )

    def get_user_info(self, user_id: int, expected_status: int = HTTPStatus.OK):
        """
        GET /user/{user_id} - Получение информации о пользователе.
        Возвращает response.
        """
        return self.requester.send_request(
            method="GET",
            endpoint=f"user/{user_id}",
            expected_status=expected_status,
            base_url=self.user_base_url
        )

    def get_current_user(self, expected_status: int = HTTPStatus.OK):
        """
        GET /user/me - Получение информации о текущем пользователе.
        """
        return self.requester.send_request(
            method="GET",
            endpoint="user/me",
            expected_status=expected_status,
            base_url=self.user_base_url
        )

    def update_user(self, user_id: int, data: Dict[str, Any], expected_status: int = HTTPStatus.OK):
        """
        PATCH /user/{user_id} - Обновление данных пользователя.
        """
        return self.requester.send_request(
            method="PATCH",
            endpoint=f"user/{user_id}",
            data=data,
            expected_status=expected_status,
            base_url=self.user_base_url
        )

    def delete_user(self, user_id: int, expected_status: int = HTTPStatus.NO_CONTENT):
        """
        DELETE /user/{user_id} - Удаление пользователя.
        """
        return self.requester.send_request(
            method="DELETE",
            endpoint=f"user/{user_id}",
            expected_status=expected_status,
            base_url=self.user_base_url
        )