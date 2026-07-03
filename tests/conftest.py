"""
Единая конфигурация для всех тестов.
Используем реальную авторизацию через AuthAPI.
"""

import pytest
import requests
from api.api_manager import ApiManager
from core.data_generator import DataGenerator

# Креды SUPER_ADMIN (из задания)
ADMIN_CREDENTIALS = {
    "username": "api1@gmail.com",
    "password": "asdqwe123Q"
}
BASE_URL = "https://api.dev-cinescope.coconutqa.ru/"


# === FIXTURES ДЛЯ СЕССИИ ===

@pytest.fixture(scope="session")
def session():
    """Создает сессию requests."""
    return requests.Session()


@pytest.fixture(scope="session")
def api_manager(session):
    """
    Создает экземпляр ApiManager с единой сессией.
    """
    return ApiManager(session, BASE_URL)


@pytest.fixture(scope="session")
def admin_token(api_manager):
    """
    Получение токена SUPER_ADMIN через AuthAPI.
    """
    token = api_manager.auth_api.get_token(
        username=ADMIN_CREDENTIALS["username"],
        password=ADMIN_CREDENTIALS["password"]
    )
    return token


@pytest.fixture(scope="session")
def public_api_manager(api_manager):
    """ApiManager без токена (для PUBLIC запросов)."""
    return api_manager


@pytest.fixture(scope="session")
def admin_api_manager(api_manager, admin_token):
    """ApiManager с токеном SUPER_ADMIN (для защищенных запросов)."""
    api_manager.set_auth_token(admin_token)
    return api_manager


# === FIXTURES ДЛЯ API ===

@pytest.fixture
def public_movies_api(public_api_manager):
    """MoviesAPI без авторизации (для GET запросов)."""
    return public_api_manager.movies_api


@pytest.fixture
def admin_movies_api(admin_api_manager):
    """MoviesAPI с авторизацией SUPER_ADMIN (для POST, DELETE, PATCH)."""
    return admin_api_manager.movies_api


@pytest.fixture
def movies_api(public_movies_api):
    """По умолчанию используем public_movies_api (для GET запросов)."""
    return public_movies_api


@pytest.fixture
def auth_api(api_manager):
    """AuthAPI для работы с авторизацией."""
    return api_manager.auth_api


@pytest.fixture
def user_api(admin_api_manager):
    """UserAPI с авторизацией SUPER_ADMIN."""
    return admin_api_manager.user_api


# === FIXTURE ДЛЯ СОЗДАНИЯ ТЕСТОВЫХ ДАННЫХ ===

@pytest.fixture
def created_movie(admin_movies_api):
    """
    Создает тестовый фильм для использования в других тестах.
    Использует admin_movies_api (с токеном).
    """
    movie_data = DataGenerator.generate_movie_data()
    response = admin_movies_api.create_movie(movie_data)
    movie_id = response.get("id")

    yield movie_id

    # Cleanup
    try:
        admin_movies_api.delete_movie(movie_id)
    except Exception as e:
        print(f"Cleanup failed for movie {movie_id}: {e}")