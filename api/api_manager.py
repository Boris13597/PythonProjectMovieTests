"""
ApiManager - управление всеми API-классами с единой HTTP-сессией.
"""

from core.custom_requester import CustomRequester
from api.auth_api import AuthAPI
from api.user_api import UserAPI
from api.movies_api import MoviesAPI


class ApiManager:
    """
    Класс для управления API-классами с единой HTTP-сессией и реквестером.
    """

    def __init__(self, session, base_url: str = "https://api.dev-cinescope.coconutqa.ru"):
        """
        Инициализация ApiManager.
        """
        self.session = session
        self.base_url = base_url.rstrip('/')  # Убираем trailing slash

        # Создаем единый реквестер для всех API
        self.requester = CustomRequester(session, self.base_url)

        # Инициализируем все API с общим реквестером
        self.auth_api = AuthAPI(self.requester)
        self.user_api = UserAPI(self.requester)
        self.movies_api = MoviesAPI(self.requester)

    def set_auth_token(self, token: str):
        """Устанавливает токен авторизации для всех API."""
        self.requester.set_auth_token(token)

    def get_requester(self):
        """Возвращает текущий реквестер для кастомизации."""
        return self.requester