"""
Единая конфигурация для всех тестов.
Используем реальную авторизацию через AuthAPI.
"""

import pytest
import requests
import random
import string
from faker import Faker

from models.base_models import TestUser
from utils.constants import HEADERS
from api.api_manager import ApiManager
from core.data_generator import DataGenerator
from entities.user import User
from resources.user_creds import SuperAdminCreds
from constans.roles import Roles

faker = Faker()

# Креды SUPER_ADMIN
ADMIN_CREDENTIALS = {
    "username": "api1@gmail.com",
    "password": "asdqwe123Q"
}

BASE_URL = "https://api.dev-cinescope.coconutqa.ru/"


# === FIXTURES ДЛЯ СЕССИИ ===

@pytest.fixture
def test_user() -> TestUser:
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER]      # указываем явно, см. ловушку exclude_unset в главе 6
    )


@pytest.fixture(scope="function")
def auth_session(test_user):
    """Создает сессию с токеном авторизованного пользователя."""
    AUTH_BASE_URL = "https://auth.dev-cinescope.coconutqa.ru"

    # Регистрируем нового пользователя
    register_url = f"{AUTH_BASE_URL}/register"
    response = requests.post(register_url, json=test_user.model_dump(), headers=HEADERS)
    assert response.status_code == 201, f"Ошибка регистрации: {response.text}"

    # Логинимся для получения токена
    login_url = f"{AUTH_BASE_URL}/login"
    login_data = {
        "email": test_user.email,
        "password": test_user.password
    }
    response = requests.post(login_url, json=login_data, headers=HEADERS)
    # ✅ Исправлено: login возвращает 200, а не 201
    assert response.status_code == 200, f"Ошибка авторизации: {response.text}"

    token = response.json().get("accessToken")
    assert token is not None, "Токен доступа отсутствует в ответе"

    session = requests.Session()
    session.headers.update(HEADERS)
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session


@pytest.fixture(scope="function")
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user, expected_status=201)
    response_data = response.json()

    # Создаем копию модели и обновляем её (для этого в TestUser должно быть поле id)
    registered_user_model = test_user.model_copy(update={"id": response_data["id"]})

    return registered_user_model


@pytest.fixture(scope="session")
def session():
    """Создает сессию requests (одна на всю тестовую сессию)."""
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    """Создает экземпляр ApiManager с единой сессией."""
    return ApiManager(session, BASE_URL)


@pytest.fixture(scope="session")
def admin_token(api_manager):
    """Получение токена SUPER_ADMIN через AuthAPI."""
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

@pytest.fixture(scope="function")
def created_movie(super_admin_movies_api):
    """Создает тестовый фильм для использования в других тестах."""
    movie_data = DataGenerator.generate_movie_data()
    response = super_admin_movies_api.create_movie(movie_data)
    movie_id = response.get("id")

    print(f"✅ Fixture created movie: {movie_id}")  # Отладка

    yield movie_id

    print(f"🗑️ Fixture deleting movie: {movie_id}")  # Отладка
    try:
        super_admin_movies_api.delete_movie(movie_id)
    except Exception as e:
        print(f"Cleanup failed for movie {movie_id}: {e}")


@pytest.fixture
def user_session():
    """Фикстура для создания пользовательских сессий."""
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_pool.append(session)
        return session

    yield _create_user_session

    for session in user_pool:
        session.close()


@pytest.fixture(scope="function")
def creation_user_data(test_user: TestUser) -> TestUser:
    return test_user.model_copy(update={"verified": True, "banned": False})


@pytest.fixture
def super_admin(user_session, api_manager):
    """Создает SUPER_ADMIN пользователя с авторизацией."""
    new_session = user_session()
    new_api_manager = ApiManager(new_session, BASE_URL)

    # Логинимся под SUPER_ADMIN
    token = new_api_manager.auth_api.get_token(
        username=SuperAdminCreds.USERNAME,
        password=SuperAdminCreds.PASSWORD
    )
    new_api_manager.set_auth_token(token)

    return User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_api_manager
    )


@pytest.fixture
def common_user(user_session, super_admin):
    """Создает обычного пользователя."""
    new_session = user_session()
    new_api_manager = ApiManager(new_session, BASE_URL)

    password = DataGenerator.generate_random_password()
    user_data = TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=password,
        passwordRepeat=password,  # ✅ Исправлено
        roles=[Roles.USER.value],
        verified=True,  # ✅ Добавлено
        banned=False  # ✅ Добавлено
    )


    super_admin.api.user_api.create_user(user_data, expected_status=201)

    user = User(
        user_data.email,
        user_data.password,
        [Roles.USER.value],
        new_api_manager
    )
    user.api.auth_api.authenticate(user.creds)
    return user


@pytest.fixture
def admin(user_session, super_admin):
    """Создает администратора."""
    new_session = user_session()
    new_api_manager = ApiManager(new_session, BASE_URL)

    password = DataGenerator.generate_random_password()
    user_data = {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": password,
        "passwordRepeat": password,  # ✅ Исправлено
        "roles": [Roles.ADMIN.value],
        "verified": True,  # ✅ Добавлено
        "banned": False  # ✅ Добавлено
    }

    response = super_admin.api.user_api.create_user(user_data, expected_status=201)
    user_id = response.json().get("id")

    # Назначаем роль ADMIN
    super_admin.api.user_api.update_user(user_id, data={"roles": ["ADMIN"]})

    user = User(
        user_data['email'],
        user_data['password'],
        [Roles.ADMIN.value],
        new_api_manager
    )
    user.api.auth_api.authenticate(user.creds)
    return user

@pytest.fixture
def super_admin_movies_api(super_admin):
    return super_admin.api.movies_api

@pytest.fixture
def admin_movies_api(admin):
    return admin.api.movies_api

@pytest.fixture
def user_movies_api(common_user):
    return common_user.api.movies_api