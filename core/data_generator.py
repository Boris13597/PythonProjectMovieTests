"""
Генератор тестовых данных для Movies API.
Использует Faker для генерации реалистичных данных.
"""

import random
import string
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from faker import Faker

faker = Faker()


class DataGenerator:
    """Генерация тестовых данных для Movies API."""

    # ==================== СУЩЕСТВУЮЩИЕ МЕТОДЫ ====================

    @staticmethod
    def generate_random_email() -> str:
        """
        Генерирует случайный email.

        Returns:
            str: Email вида kek{random}@gmail.com
        """
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_random_name() -> str:
        """
        Генерирует случайное полное имя.

        Returns:
            str: Имя и фамилия
        """
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_password() -> str:
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 заглавная буква.
        - Минимум 1 строчная буква.
        - Минимум 1 цифра.
        - Минимум 1 спецсимвол.
        - Длина от 8 до 20 символов.

        Returns:
            str: Сгенерированный пароль
        """
        # Гарантируем наличие хотя бы одной буквы и одной цифры
        lowercase = random.choice(string.ascii_lowercase)
        uppercase = random.choice(string.ascii_uppercase)
        digits = random.choice(string.digits)

        # Дополняем пароль случайными символами из допустимого набора
        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        # Перемешиваем пароль для рандомизации
        password = list(uppercase + lowercase + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    # ==================== НОВЫЕ МЕТОДЫ ДЛЯ MOVIES API ====================

    @staticmethod
    def generate_string(length: int = 10) -> str:
        """
        Генерирует случайную строку из букв.

        Args:
            length: Длина строки

        Returns:
            str: Случайная строка
        """
        return ''.join(random.choices(string.ascii_letters, k=length))

    @staticmethod
    def generate_unique_movie_name() -> str:
        """
        Генерирует уникальное название фильма с временной меткой.

        Returns:
            str: Уникальное название фильма
        """
        return f"Movie_{DataGenerator.generate_string(8)}_{int(datetime.now().timestamp())}"

    @staticmethod
    def generate_movie_data(custom_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Генерирует данные для создания фильма.

        Args:
            custom_data: Словарь с кастомными значениями для переопределения

        Returns:
            Dict с данными для создания фильма
        """
        data = {
            "name": f"Test Movie {DataGenerator.generate_string(5)}",
            "imageUrl": "https://dummyimage.com/1020x260",
            "price": round(random.uniform(100, 900), 2),
            "description": faker.text(max_nb_chars=50),
            "location": random.choice(["MSK", "SPB"]),
            "published": random.choice([True, False]),
            "genreId": random.randint(1, 5)
        }

        # Переопределяем кастомными значениями, если переданы
        if custom_data:
            data.update(custom_data)

        return data

    @staticmethod
    def generate_edit_movie_data() -> Dict[str, Any]:
        """
        Генерирует данные для редактирования фильма.

        Returns:
            Dict с данными для обновления фильма
        """
        return {
            "name": f"Updated Movie {DataGenerator.generate_string(5)}",
            "description": faker.text(max_nb_chars=30),
            "price": round(random.uniform(150, 850), 2)
        }

    @staticmethod
    def generate_invalid_movie_data() -> Dict[str, Any]:
        """
        Генерирует данные с невалидными значениями для негативных тестов.

        Returns:
            Dict с невалидными данными
        """
        return {
            "name": "",
            "imageUrl": "not_a_url",
            "price": -100,
            "description": "",
            "location": "INVALID",
            "published": "not_boolean",
            "genreId": 99999
        }

    @staticmethod
    def generate_filter_params() -> Dict[str, Any]:
        """
        Генерирует случайные параметры для фильтрации фильмов.

        Returns:
            Dict с параметрами фильтрации
        """
        locations = random.sample(["MSK", "SPB"], k=random.randint(1, 2))
        return {
            "pageSize": random.choice([5, 10, 20, 50]),
            "page": random.randint(1, 3),
            "minPrice": random.randint(1, 100),
            "maxPrice": random.randint(500, 1000),
            "locations": locations,
            "published": random.choice([True, False]),
            "genreId": random.randint(1, 5),
            "createdAt": random.choice(["asc", "desc"])
        }

    @staticmethod
    def generate_movie_with_specific_location(location: str) -> Dict[str, Any]:
        """
        Генерирует данные фильма с конкретной локацией.

        Args:
            location: Локация (MSK или SPB)

        Returns:
            Dict с данными фильма
        """
        return DataGenerator.generate_movie_data({"location": location})

    @staticmethod
    def generate_movie_with_specific_genre(genre_id: int) -> Dict[str, Any]:
        """
        Генерирует данные фильма с конкретным жанром.

        Args:
            genre_id: ID жанра

        Returns:
            Dict с данными фильма
        """
        return DataGenerator.generate_movie_data({"genreId": genre_id})

    @staticmethod
    def generate_movie_with_price_range(min_price: float, max_price: float) -> Dict[str, Any]:
        """
        Генерирует данные фильма с ценой в указанном диапазоне.

        Args:
            min_price: Минимальная цена
            max_price: Максимальная цена

        Returns:
            Dict с данными фильма
        """
        price = round(random.uniform(min_price, max_price), 2)
        return DataGenerator.generate_movie_data({"price": price})

    @staticmethod
    def generate_movie_with_published_status(published: bool) -> Dict[str, Any]:
        """
        Генерирует данные фильма с конкретным статусом публикации.

        Args:
            published: Статус публикации

        Returns:
            Dict с данными фильма
        """
        return DataGenerator.generate_movie_data({"published": published})

    @staticmethod
    def generate_multiple_movies(count: int = 3) -> List[Dict[str, Any]]:
        """
        Генерирует список данных для нескольких фильмов.

        Args:
            count: Количество фильмов для генерации

        Returns:
            List[Dict] с данными фильмов
        """
        return [DataGenerator.generate_movie_data() for _ in range(count)]

    @staticmethod
    def generate_review_data() -> Dict[str, Any]:
        """
        Генерирует данные для создания отзыва.

        Returns:
            Dict с данными отзыва
        """
        return {
            "rating": random.randint(1, 5),
            "text": faker.text(max_nb_chars=100)
        }

    @staticmethod
    def generate_user_data() -> Dict[str, Any]:
        """
        Генерирует данные для регистрации пользователя.

        Returns:
            Dict с данными пользователя
        """
        return {
            "username": DataGenerator.generate_random_email(),
            "password": DataGenerator.generate_random_password(),
            "fullName": DataGenerator.generate_random_name()
        }

    @staticmethod
    def generate_long_text(length: int = 1000) -> str:
        """
        Генерирует длинный текст для тестирования граничных значений.

        Args:
            length: Длина текста

        Returns:
            str: Длинный текст
        """
        return 'A' * length

    @staticmethod
    def generate_special_characters_string() -> str:
        """
        Генерирует строку со спецсимволами.

        Returns:
            str: Строка со спецсимволами
        """
        special_chars = "!@#$%^&*()_+{}|:<>?~"
        return f"Movie{''.join(random.choices(special_chars, k=3))}Test"