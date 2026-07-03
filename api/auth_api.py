"""API класс для авторизации."""

from typing import Dict, Any, Optional
from api.base_api import BaseAPI
from http import HTTPStatus


class AuthAPI(BaseAPI):
    """
    API-класс для авторизации и получения токена.
    Базовый URL: https://auth.dev-cinescope.coconutqa.ru
    """

    def __init__(self, requester):
        self.requester = requester
        self.auth_base_url = "https://auth.dev-cinescope.coconutqa.ru"

    def login(self, credentials: Dict[str, Any], expected_status: int = HTTPStatus.CREATED) -> Dict[str, Any]:
        """
        POST /login - Авторизация пользователя.
        Возвращает 201 Created при успешном логине.
        """
        login_data = {
            "email": credentials.get("username") or credentials.get("email"),
            "password": credentials.get("password")
        }

        response = self.requester.send_request(
            method="POST",
            endpoint="login",
            data=login_data,
            expected_status=expected_status,
            base_url=self.auth_base_url
        )
        return response.json()

    def register(self, user_data: Dict[str, Any], expected_status: int = HTTPStatus.CREATED) -> Dict[str, Any]:
        response = self.requester.send_request(
            method="POST",
            endpoint="register",
            data=user_data,
            expected_status=expected_status,
            base_url=self.auth_base_url
        )
        return response.json()

    def get_token(self, username: str, password: str) -> str:
        """Получение токена для пользователя."""
        login_data = {"email": username, "password": password}
        response = self.requester.send_request(
            method="POST",
            endpoint="login",
            data=login_data,
            expected_status=HTTPStatus.CREATED,  # 201 Created!
            base_url=self.auth_base_url
        )
        response_data = response.json()

        token = response_data.get("accessToken") or response_data.get("access_token")
        if not token:
            raise ValueError(f"Token not found in response: {response_data}")

        return token