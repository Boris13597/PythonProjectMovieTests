"""API класс для работы с пользователями."""

from typing import Dict, Any, Optional
from api.base_api import BaseAPI
from http import HTTPStatus


class UserAPI(BaseAPI):
    """
    API-класс для работы с пользователями.
    Базовый URL: https://auth.dev-cinescope.coconutqa.ru/
    """

    def __init__(self, requester):
        """
        Инициализация UserAPI.
        Использует тот же requester, но с другим base_url.
        """
        self.requester = requester
        # Для UserAPI используем другой base_url
        self.user_base_url = "https://auth.dev-cinescope.coconutqa.ru/"

    def get_user_info(self, user_id: int, expected_status: int = HTTPStatus.OK) -> Dict[str, Any]:
        """
        GET /user/{user_id} - Получение информации о пользователе.

        Args:
            user_id: ID пользователя
            expected_status: Ожидаемый статус-код

        Returns:
            Dict с данными пользователя
        """
        response = self.requester.send_request(
            method="GET",
            endpoint=f"/user/{user_id}",
            expected_status=expected_status,
            base_url=self.user_base_url
        )
        return response.json()

    def delete_user(self, user_id: int, expected_status: int = HTTPStatus.NO_CONTENT) -> Dict[str, Any]:
        """
        DELETE /user/{user_id} - Удаление пользователя.

        Args:
            user_id: ID пользователя для удаления
            expected_status: Ожидаемый статус-код

        Returns:
            Dict с результатом удаления
        """
        response = self.requester.send_request(
            method="DELETE",
            endpoint=f"/user/{user_id}",
            expected_status=expected_status,
            base_url=self.user_base_url
        )
        return response.json()

    def get_current_user(self, expected_status: int = HTTPStatus.OK) -> Dict[str, Any]:
        """
        GET /user/me - Получение информации о текущем пользователе.

        Returns:
            Dict с данными текущего пользователя
        """
        response = self.requester.send_request(
            method="GET",
            endpoint="/user/me",
            expected_status=expected_status,
            base_url=self.user_base_url
        )
        return response.json()

    def update_user(self, user_id: int, data: Dict[str, Any], expected_status: int = HTTPStatus.OK) -> Dict[str, Any]:
        """
        PATCH /user/{user_id} - Обновление данных пользователя.

        Args:
            user_id: ID пользователя
            data: Данные для обновления
            expected_status: Ожидаемый статус-код

        Returns:
            Dict с обновленными данными пользователя
        """
        response = self.requester.send_request(
            method="PATCH",
            endpoint=f"/user/{user_id}",
            data=data,
            expected_status=expected_status,
            base_url=self.user_base_url
        )
        return response.json()