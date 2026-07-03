"""
Тесты для DELETE /movies/{id} - Удаление фильма
"""
import time
import pytest
from core.data_generator import DataGenerator
from http import HTTPStatus


class TestMoviesDelete:
    """Тесты для DELETE /movies/{id} - Удаление фильма."""

    def test_delete_movie_success(self, admin_movies_api, public_movies_api):
        """Позитивный тест: успешное удаление фильма."""
        movie_data = DataGenerator.generate_movie_data()
        create_response = admin_movies_api.create_movie(movie_data)
        movie_id = create_response["id"]

        get_response = public_movies_api.get_movie_by_id(movie_id)
        assert get_response["id"] == movie_id

        delete_response = admin_movies_api.delete_movie(movie_id)

        assert delete_response["id"] == movie_id
        assert delete_response["name"] == movie_data["name"]
        assert delete_response["price"] == int(movie_data["price"])
        assert "genre" in delete_response
        assert "createdAt" in delete_response

        with pytest.raises(ValueError) as excinfo:
            public_movies_api.get_movie_by_id(movie_id)

        assert "404" in str(excinfo.value)

    def test_delete_movie_return_all_fields(self, admin_movies_api):
        """Позитивный тест: проверка, что DELETE возвращает все поля удаленного фильма."""
        movie_data = {
            "name": f"Delete Check {DataGenerator.generate_string(5)}",
            "imageUrl": "https://dummyimage.com/1020x260",
            "price": 555,
            "description": f"Description for delete {DataGenerator.generate_string(10)}",
            "location": "MSK",
            "published": True,
            "genreId": 3
        }

        create_response = admin_movies_api.create_movie(movie_data)
        movie_id = create_response["id"]

        delete_response = admin_movies_api.delete_movie(movie_id)

        expected_fields = [
            "id", "name", "price", "description", "imageUrl",
            "location", "published", "genreId", "genre",
            "createdAt", "rating"
        ]

        for field in expected_fields:
            assert field in delete_response, f"Missing field in DELETE response: {field}"

        assert delete_response["id"] == movie_id
        assert delete_response["name"] == movie_data["name"]
        assert delete_response["price"] == int(movie_data["price"])

    def test_delete_movie_multiple_times(self, admin_movies_api):
        """Негативный тест: удаление фильма, который уже был удален ранее."""
        movie_data = DataGenerator.generate_movie_data()
        create_response = admin_movies_api.create_movie(movie_data)
        movie_id = create_response["id"]

        delete_response = admin_movies_api.delete_movie(movie_id)
        assert delete_response["id"] == movie_id

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.delete_movie(movie_id)

        assert "404" in str(excinfo.value)

    def test_delete_movie_verify_data_types(self, admin_movies_api):
        """Позитивный тест: проверка типов данных в ответе DELETE."""
        movie_data = DataGenerator.generate_movie_data()
        create_response = admin_movies_api.create_movie(movie_data)
        movie_id = create_response["id"]

        delete_response = admin_movies_api.delete_movie(movie_id)

        assert isinstance(delete_response["id"], int)
        assert isinstance(delete_response["name"], str)
        assert isinstance(delete_response["price"], (int, float))
        assert isinstance(delete_response["description"], str)
        assert isinstance(delete_response["imageUrl"], str)
        assert isinstance(delete_response["location"], str)
        assert isinstance(delete_response["published"], bool)
        assert isinstance(delete_response["genreId"], int)
        assert isinstance(delete_response["rating"], (int, float))
        assert isinstance(delete_response["createdAt"], str)

    def test_delete_movie_check_rating_value(self, admin_movies_api):
        """Позитивный тест: проверка, что рейтинг в ответе DELETE в допустимом диапазоне."""
        movie_data = DataGenerator.generate_movie_data()
        create_response = admin_movies_api.create_movie(movie_data)
        movie_id = create_response["id"]

        delete_response = admin_movies_api.delete_movie(movie_id)

        rating = delete_response["rating"]
        assert 0 <= rating <= 10, f"Rating {rating} out of expected range"

    def test_delete_movie_check_genre_structure(self, admin_movies_api):
        """Позитивный тест: проверка структуры жанра в ответе DELETE."""
        movie_data = DataGenerator.generate_movie_data()
        create_response = admin_movies_api.create_movie(movie_data)
        movie_id = create_response["id"]

        delete_response = admin_movies_api.delete_movie(movie_id)

        assert "genre" in delete_response
        assert "name" in delete_response["genre"]
        assert isinstance(delete_response["genre"]["name"], str)

    # ==================== НЕГАТИВНЫЕ ТЕСТЫ ====================

    def test_delete_movie_not_found(self, admin_movies_api):
        """Негативный тест: удаление несуществующего фильма."""
        fake_id = 999999999

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.delete_movie(fake_id)

        assert "404" in str(excinfo.value)

    def test_delete_movie_negative_id(self, admin_movies_api):
        """Негативный тест: удаление с отрицательным ID."""
        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.delete_movie(-1)

        assert "400" in str(excinfo.value) or "404" in str(excinfo.value)

    def test_delete_movie_zero_id(self, admin_movies_api):
        """Негативный тест: удаление с ID = 0."""
        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.delete_movie(0)

        assert "400" in str(excinfo.value) or "404" in str(excinfo.value)

    def test_delete_movie_string_id(self, admin_movies_api):
        """Негативный тест: удаление с ID в виде строки."""
        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.delete_movie("not_a_number")

        assert "400" in str(excinfo.value) or "404" in str(excinfo.value)

    def test_delete_movie_empty_id(self, admin_movies_api):
        """Негативный тест: удаление с пустым ID."""
        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.delete_movie("")

        assert "400" in str(excinfo.value) or "404" in str(excinfo.value)

    def test_delete_movie_very_large_id(self, admin_movies_api):
        """Негативный тест: удаление с очень большим ID."""
        large_id = 999999999999999999

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.delete_movie(large_id)

        assert "400" in str(excinfo.value) or "404" in str(excinfo.value)

    def test_delete_movie_float_id(self, admin_movies_api):
        """Негативный тест: удаление с ID в виде числа с плавающей точкой."""
        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.delete_movie(123.45)

        assert "400" in str(excinfo.value) or "404" in str(excinfo.value)

    # ==================== ИНТЕГРАЦИОННЫЕ ТЕСТЫ ====================

    def test_delete_movie_full_lifecycle(self, admin_movies_api, public_movies_api):
        """Интеграционный тест: полный жизненный цикл с удалением."""
        movie_data = DataGenerator.generate_movie_data()
        create_response = admin_movies_api.create_movie(movie_data)
        movie_id = create_response["id"]
        assert create_response["id"] == movie_id

        get_response = public_movies_api.get_movie_by_id(movie_id)
        assert get_response["id"] == movie_id

        delete_response = admin_movies_api.delete_movie(movie_id)
        assert delete_response["id"] == movie_id
        assert delete_response["name"] == movie_data["name"]

        with pytest.raises(ValueError) as excinfo:
            public_movies_api.get_movie_by_id(movie_id)

        assert "404" in str(excinfo.value)

    def test_delete_movie_and_verify_in_list(self, admin_movies_api, public_movies_api):
        """
        Интеграционный тест: проверка, что после удаления фильм недоступен по ID.
        """
        unique_name = f"UniqueMovie_{DataGenerator.generate_string(8)}_{int(time.time())}"
        movie_data = DataGenerator.generate_movie_data({"name": unique_name})
        create_response = admin_movies_api.create_movie(movie_data)
        movie_id = create_response["id"]

        # Проверяем, что фильм доступен по ID
        get_response = public_movies_api.get_movie_by_id(movie_id)
        assert get_response["id"] == movie_id
        assert get_response["name"] == unique_name

        # Удаляем фильм
        delete_response = admin_movies_api.delete_movie(movie_id)
        assert delete_response["id"] == movie_id

        # Проверяем, что после удаления фильм НЕ доступен по ID
        with pytest.raises(ValueError) as excinfo:
            public_movies_api.get_movie_by_id(movie_id)
        assert "404" in str(excinfo.value)

    def test_delete_movie_check_created_at_unchanged(self, admin_movies_api):
        """Интеграционный тест: проверка, что createdAt не меняется при удалении."""
        movie_data = DataGenerator.generate_movie_data()
        create_response = admin_movies_api.create_movie(movie_data)
        movie_id = create_response["id"]
        created_at = create_response["createdAt"]

        delete_response = admin_movies_api.delete_movie(movie_id)
        assert delete_response["createdAt"] == created_at

    def test_delete_movie_check_all_fields_preserved(self, admin_movies_api):
        """Интеграционный тест: проверка, что все поля сохраняются в ответе DELETE."""
        movie_data = {
            "name": f"Full Delete {DataGenerator.generate_string(5)}",
            "imageUrl": "https://dummyimage.com/1020x260",
            "price": 999,
            "description": f"Full description {DataGenerator.generate_string(15)}",
            "location": "SPB",
            "published": True,
            "genreId": 4
        }

        create_response = admin_movies_api.create_movie(movie_data)
        movie_id = create_response["id"]

        delete_response = admin_movies_api.delete_movie(movie_id)

        assert delete_response["id"] == movie_id
        assert delete_response["name"] == movie_data["name"]
        assert delete_response["imageUrl"] == movie_data["imageUrl"]
        assert delete_response["price"] == int(movie_data["price"])
        assert delete_response["description"] == movie_data["description"]
        assert delete_response["location"] == movie_data["location"]
        assert delete_response["published"] == movie_data["published"]
        assert delete_response["genreId"] == movie_data["genreId"]
        assert "createdAt" in delete_response
        assert "rating" in delete_response

    def test_delete_movie_verify_no_reviews(self, admin_movies_api):
        """Интеграционный тест: проверка, что отзывы не возвращаются в DELETE."""
        movie_data = DataGenerator.generate_movie_data()
        create_response = admin_movies_api.create_movie(movie_data)
        movie_id = create_response["id"]

        delete_response = admin_movies_api.delete_movie(movie_id)

        assert "reviews" not in delete_response or delete_response["reviews"] == []