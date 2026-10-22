# api/auth_api.py

from typing import Dict, Any
from http import HTTPStatus


class AuthAPI:
    """
    API-класс для авторизации и получения токена.
    Базовый URL: https://auth.dev-cinescope.coconutqa.ru
    """

    def __init__(self, requester):
        self.requester = requester
        self.auth_base_url = "https://auth.dev-cinescope.coconutqa.ru"

    # api/auth_api.py - исправленный метод login

    def login(self, credentials: Dict[str, Any], expected_status: int = HTTPStatus.OK) -> Dict[str, Any]:
        """
        POST /login - Авторизация пользователя.
        Возвращает 200 OK при успешном логине.
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
        """
        POST /register - Регистрация пользователя.
        """
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
            expected_status=[HTTPStatus.OK, HTTPStatus.CREATED],
            base_url=self.auth_base_url
        )
        response_data = response.json()

        token = response_data.get("accessToken") or response_data.get("access_token")
        if not token:
            raise ValueError(f"Token not found in response: {response_data}")

        return token

    def authenticate(self, user_creds):
        """
        Аутентификация пользователя и получение токена.
        """
        login_data = {
            "email": user_creds[0],
            "password": user_creds[1]
        }
        response = self.requester.send_request(
            method="POST",
            endpoint="login",
            data=login_data,
            expected_status=[HTTPStatus.OK, HTTPStatus.CREATED],
            base_url=self.auth_base_url
        )
        response_data = response.json()

        if "accessToken" not in response_data:
            raise KeyError("token is missing")

        token = response_data["accessToken"]
        self.requester.set_auth_token(token)
        return token

    # === МЕТОДЫ ДЛЯ ТЕСТОВ ===

    def register_user(self, user_data: Dict[str, Any], expected_status: int = HTTPStatus.CREATED):
        """
        Метод для тестов: регистрация пользователя.
        Возвращает response (не response.json()).
        """
        return self.requester.send_request(
            method="POST",
            endpoint="register",
            data=user_data,
            expected_status=expected_status,
            base_url=self.auth_base_url
        )

    def login_user(self, login_data: Dict[str, Any], expected_status: int = None):
        """
        Метод для тестов: авторизация пользователя.
        Если expected_status не указан, не проверяет статус и не выбрасывает исключение.
        """
        try:
            return self.requester.send_request(
                method="POST",
                endpoint="login",
                data=login_data,
                expected_status=expected_status,
                base_url=self.auth_base_url
            )
        except ValueError:
            # Если expected_status не указан, возвращаем response даже с ошибкой
            if expected_status is None:
                # Делаем запрос заново без проверки статуса
                return self.requester.send_request(
                    method="POST",
                    endpoint="login",
                    data=login_data,
                    expected_status=None,
                    base_url=self.auth_base_url
                )
            raise