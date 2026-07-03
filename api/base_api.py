"""Базовый класс для всех API классов."""

from core.custom_requester import CustomRequester


class BaseAPI:
    """Базовый класс для API-классов."""

    def __init__(self, requester: CustomRequester):
        """
        Инициализация API-класса.

        Args:
            requester: Экземпляр CustomRequester для отправки запросов
        """
        self.requester = requester

    def set_token(self, token: str):
        """
        Устанавливает токен авторизации для текущего API.

        Args:
            token: JWT токен
        """
        self.requester.set_auth_token(token)