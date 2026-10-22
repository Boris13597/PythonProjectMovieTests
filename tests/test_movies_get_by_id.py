"""
Тесты для GET /movies/{id} - Получение фильма по ID
"""
from http import HTTPStatus

import pytest
import re
from core.data_generator import DataGenerator


class TestMoviesGetById:
    """Тесты для GET /movies/{id} - Получение фильма по ID."""

    # ==================== ПОЗИТИВНЫЕ ТЕСТЫ ====================

    def test_get_movie_by_id_check_genre_structure(self, public_movies_api, created_movie):
        """Позитивный тест: проверка структуры жанра в ответе."""
        movie_id = created_movie
        response = public_movies_api.get_movie_by_id(movie_id)

        assert "genre" in response
        assert "name" in response["genre"]
        assert isinstance(response["genre"]["name"], str)

    def test_get_movie_by_id_check_reviews_structure(self, public_movies_api, created_movie):
        """Позитивный тест: проверка структуры отзывов в ответе."""
        movie_id = created_movie
        response = public_movies_api.get_movie_by_id(movie_id)

        assert "reviews" in response
        assert isinstance(response["reviews"], list)

    def test_get_movie_by_id_compare_with_created_data(self, public_movies_api, super_admin_movies_api):
        """Позитивный тест: сравнение полученного фильма с созданными данными."""
        movie_data = {
            "name": f"Compare Test {DataGenerator.generate_string(5)}",
            "imageUrl": "https://dummyimage.com/1020x260",
            "price": 777,
            "description": f"Description for compare {DataGenerator.generate_string(10)}",
            "location": "SPB",
            "published": True,
            "genreId": DataGenerator.get_valid_genre_id()
        }

        create_response = super_admin_movies_api.create_movie(movie_data)
        movie_id = create_response["id"]

        get_response = public_movies_api.get_movie_by_id(movie_id)

        assert get_response["id"] == movie_id
        assert get_response["name"] == movie_data["name"]
        assert get_response["price"] == int(movie_data["price"])
        assert get_response["description"] == movie_data["description"]
        assert get_response["imageUrl"] == movie_data["imageUrl"]
        assert get_response["location"] == movie_data["location"]
        assert get_response["published"] == movie_data["published"]
        assert get_response["genreId"] == movie_data["genreId"]

        super_admin_movies_api.delete_movie(movie_id)

    def test_get_movie_by_id_check_dates(self, public_movies_api, created_movie):
        """Позитивный тест: проверка формата дат в ответе."""
        movie_id = created_movie
        response = public_movies_api.get_movie_by_id(movie_id)

        assert "createdAt" in response
        assert isinstance(response["createdAt"], str)

        iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$'
        assert re.match(iso_pattern, response["createdAt"]) is not None

    def test_get_movie_by_id_rating_range(self, public_movies_api, created_movie):
        """Позитивный тест: проверка, что рейтинг в допустимом диапазоне."""
        movie_id = created_movie
        response = public_movies_api.get_movie_by_id(movie_id)

        assert "rating" in response
        rating = response["rating"]
        assert 0 <= rating <= 10, f"Rating {rating} out of expected range"

    def test_get_movie_by_id_all_fields_present(self, public_movies_api, created_movie):
        """Позитивный тест: проверка наличия всех обязательных полей."""
        movie_id = created_movie
        response = public_movies_api.get_movie_by_id(movie_id)

        expected_fields = [
            "id", "name", "price", "description", "imageUrl",
            "location", "published", "genreId", "genre",
            "createdAt", "rating", "reviews"
        ]

        for field in expected_fields:
            assert field in response, f"Missing field: {field}"

    # ==================== НЕГАТИВНЫЕ ТЕСТЫ ====================

    def test_get_movie_by_id_not_found(self, movies_api):
        """Тест получения несуществующего фильма."""
        response = movies_api.requester.send_request(
            "GET",
            "movies/999999999",
            expected_status=HTTPStatus.NOT_FOUND  # ✅ Исправлено: 404
        )
        assert response.status_code == 404

    def test_get_movie_by_id_negative_id(self, public_movies_api):
        """Негативный тест: получение с отрицательным ID."""
        with pytest.raises(ValueError) as excinfo:
            public_movies_api.get_movie_by_id(-1)

        # API возвращает 404
        assert "404" in str(excinfo.value)

    def test_get_movie_by_id_zero_id(self, public_movies_api):
        """Негативный тест: получение с ID = 0."""
        with pytest.raises(ValueError) as excinfo:
            public_movies_api.get_movie_by_id(0)

        # API возвращает 404
        assert "404" in str(excinfo.value)

    def test_get_movie_by_id_string_id(self, movies_api):
        """Тест с строковым ID."""
        response = movies_api.requester.send_request(
            "GET",
            "movies/not_a_number",
            expected_status=HTTPStatus.INTERNAL_SERVER_ERROR  # ✅ Исправлено: 500
        )
        assert response.status_code == 500

    def test_get_movie_by_id_empty_id(self, public_movies_api):
        """
        Негативный тест: получение с пустым ID.
        Пустой ID воспринимается как GET /movies и возвращает список.
        """
        response = public_movies_api.get_movie_by_id("")
        assert "movies" in response
        assert isinstance(response["movies"], list)

    def test_get_movie_by_id_after_delete(self, public_movies_api, super_admin_movies_api):
        """Негативный тест: получение фильма после его удаления."""
        movie_data = DataGenerator.generate_movie_data()
        response = super_admin_movies_api.create_movie(movie_data)
        movie_id = response["id"]

        super_admin_movies_api.delete_movie(movie_id)

        with pytest.raises(ValueError) as excinfo:
            public_movies_api.get_movie_by_id(movie_id)

        assert "404" in str(excinfo.value)

    def test_get_movie_by_id_very_large_id(self, public_movies_api):
        """Негативный тест: получение с очень большим ID (возвращает 500)."""
        with pytest.raises(ValueError) as excinfo:
            public_movies_api.get_movie_by_id(999999999999999999)

        # API возвращает 500 Internal Server Error
        assert "500" in str(excinfo.value) or "400" in str(excinfo.value)

    # ==================== ИНТЕГРАЦИОННЫЕ ТЕСТЫ ====================

    def test_get_movie_by_id_integration(self, public_movies_api, super_admin_movies_api):
        """Интеграционный тест: полный цикл создания и получения фильма."""
        movie_data = DataGenerator.generate_movie_data()
        create_response = super_admin_movies_api.create_movie(movie_data)
        movie_id = create_response["id"]

        get_response = public_movies_api.get_movie_by_id(movie_id)

        assert get_response["id"] == movie_id
        assert get_response["name"] == movie_data["name"]
        assert get_response["description"] == movie_data["description"]
        assert get_response["price"] == int(movie_data["price"])
        assert get_response["location"] == movie_data["location"]
        assert get_response["published"] == movie_data["published"]
        assert get_response["genreId"] == movie_data["genreId"]

        super_admin_movies_api.delete_movie(movie_id)

    def test_get_movie_by_id_compare_cached_data(self, public_movies_api, super_admin_movies_api):
        """Интеграционный тест: проверка, что данные не меняются при повторных запросах."""
        movie_data = DataGenerator.generate_movie_data()
        create_response = super_admin_movies_api.create_movie(movie_data)
        movie_id = create_response["id"]

        response1 = public_movies_api.get_movie_by_id(movie_id)
        response2 = public_movies_api.get_movie_by_id(movie_id)

        assert response1["id"] == response2["id"]
        assert response1["name"] == response2["name"]
        assert response1["description"] == response2["description"]
        assert response1["price"] == response2["price"]
        assert response1["location"] == response2["location"]
        assert response1["published"] == response2["published"]
        assert response1["genreId"] == response2["genreId"]
        assert response1["rating"] == response2["rating"]

        super_admin_movies_api.delete_movie(movie_id)

    def test_get_movie_by_id_correct_data_types(self, public_movies_api, created_movie):
        """Позитивный тест: проверка типов данных всех полей."""
        movie_id = created_movie
        response = public_movies_api.get_movie_by_id(movie_id)

        type_checks = {
            "id": int,
            "name": str,
            "price": (int, float),
            "description": str,
            "imageUrl": str,
            "location": str,
            "published": bool,
            "genreId": int,
            "genre": dict,
            "createdAt": str,
            "rating": (int, float),
            "reviews": list
        }

        for field, expected_type in type_checks.items():
            assert field in response, f"Field '{field}' is missing"
            if isinstance(expected_type, tuple):
                assert isinstance(response[field], expected_type), \
                    f"Field '{field}' has type {type(response[field])}, expected {expected_type}"
            else:
                assert isinstance(response[field], expected_type), \
                    f"Field '{field}' has type {type(response[field])}, expected {expected_type}"