"""
Тесты для POST /movies - Создание фильма
"""
import pytest
from core.data_generator import DataGenerator


class TestMoviesPost:
    """Тесты для POST /movies - Создание фильма."""

    # ==================== ПОЗИТИВНЫЕ ТЕСТЫ ====================

    def test_create_movie_success(self, super_admin_movies_api):
        """Позитивный тест: успешное создание фильма."""
        movie_data = DataGenerator.generate_movie_data()
        response = super_admin_movies_api.create_movie(movie_data)

        assert "id" in response
        assert response["name"] == movie_data["name"]
        assert response["description"] == movie_data["description"]
        assert response["price"] == int(movie_data["price"])
        assert response["location"] == movie_data["location"]
        assert response["published"] == movie_data["published"]
        assert response["genreId"] == movie_data["genreId"]
        assert "createdAt" in response
        assert "genre" in response

        movie_id = response["id"]
        get_response = super_admin_movies_api.get_movie_by_id(movie_id)
        assert get_response["id"] == movie_id

        super_admin_movies_api.delete_movie(movie_id)

    def test_create_movie_with_custom_data(self, super_admin_movies_api):
        """Позитивный тест: создание фильма с кастомными значениями."""
        # ✅ Используем валидный genreId из DataGenerator
        custom_data = {
            "name": f"Custom Movie {DataGenerator.generate_string(5)}",
            "price": 500,
            "location": "MSK",
            "published": True,
            "genreId": DataGenerator.get_valid_genre_id()
        }
        movie_data = DataGenerator.generate_movie_data(custom_data)
        response = super_admin_movies_api.create_movie(movie_data)

        assert response["name"] == custom_data["name"]
        assert response["price"] == custom_data["price"]
        assert response["location"] == custom_data["location"]
        assert response["published"] == custom_data["published"]
        assert response["genreId"] == custom_data["genreId"]

        super_admin_movies_api.delete_movie(response["id"])

    def test_create_movie_with_all_fields(self, super_admin_movies_api):
        """Позитивный тест: создание со всеми полями."""
        # ✅ Используем валидные значения из DataGenerator
        movie_data = {
            "name": f"Full Movie {DataGenerator.generate_string(6)}",
            "imageUrl": "https://example.com/poster.jpg",
            "price": 350,
            "description": f"Full description {DataGenerator.generate_string(20)}",
            "location": DataGenerator.get_valid_location(),
            "published": True,
            "genreId": DataGenerator.get_valid_genre_id()
        }

        response = super_admin_movies_api.create_movie(movie_data)
        movie_id = response["id"]

        assert response["name"] == movie_data["name"]
        assert response["imageUrl"] == movie_data["imageUrl"]
        assert response["price"] == movie_data["price"]
        assert response["description"] == movie_data["description"]
        assert response["location"] == movie_data["location"]
        assert response["published"] == movie_data["published"]
        assert response["genreId"] == movie_data["genreId"]
        assert response["rating"] is not None

        super_admin_movies_api.delete_movie(movie_id)

    def test_create_movie_with_different_locations(self, super_admin_movies_api):
        """Позитивный тест: создание фильмов в разных локациях."""
        for location in DataGenerator.VALID_LOCATIONS:
            movie_data = DataGenerator.generate_movie_data({"location": location})
            response = super_admin_movies_api.create_movie(movie_data)
            movie_id = response["id"]

            assert response["location"] == location
            super_admin_movies_api.delete_movie(movie_id)

    def test_create_movie_with_different_published_status(self, super_admin_movies_api):
        """Позитивный тест: создание с разными статусами публикации."""
        for published_status in [True, False]:
            movie_data = DataGenerator.generate_movie_data({"published": published_status})
            response = super_admin_movies_api.create_movie(movie_data)
            movie_id = response["id"]

            assert response["published"] == published_status
            super_admin_movies_api.delete_movie(movie_id)

    def test_create_movie_special_characters(self, super_admin_movies_api):
        """Позитивный тест: создание с названием, содержащим спецсимволы."""
        special_name = DataGenerator.generate_special_characters_string()
        movie_data = DataGenerator.generate_movie_data({"name": special_name})
        response = super_admin_movies_api.create_movie(movie_data)
        movie_id = response["id"]

        assert response["name"] == special_name
        super_admin_movies_api.delete_movie(movie_id)

    def test_create_movie_missing_image_url(self, super_admin_movies_api):
        """
        Позитивный тест: создание без imageUrl (API допускает null).
        """
        movie_data = DataGenerator.generate_movie_data()
        del movie_data["imageUrl"]

        response = super_admin_movies_api.create_movie(movie_data)
        assert "id" in response
        assert response["imageUrl"] is None

        super_admin_movies_api.delete_movie(response["id"])

    def test_create_movie_negative_price(self, super_admin_movies_api):
        """
        Позитивный тест: создание с отрицательной ценой (API допускает).
        """
        movie_data = DataGenerator.generate_movie_data({"price": -100})
        response = super_admin_movies_api.create_movie(movie_data)

        assert "id" in response
        assert response["price"] == -100

        super_admin_movies_api.delete_movie(response["id"])

    def test_create_movie_zero_price(self, super_admin_movies_api):
        """
        Позитивный тест: создание с нулевой ценой (API допускает).
        """
        movie_data = DataGenerator.generate_movie_data({"price": 0})
        response = super_admin_movies_api.create_movie(movie_data)

        assert "id" in response
        assert response["price"] == 0

        super_admin_movies_api.delete_movie(response["id"])

    def test_create_movie_empty_description(self, super_admin_movies_api):
        """
        Позитивный тест: создание с пустым описанием (API допускает).
        """
        movie_data = DataGenerator.generate_movie_data({"description": ""})
        response = super_admin_movies_api.create_movie(movie_data)

        assert "id" in response
        assert response["description"] == ""

        super_admin_movies_api.delete_movie(response["id"])

    def test_create_movie_very_large_price(self, super_admin_movies_api):
        """Позитивный тест: очень большая цена."""
        movie_data = DataGenerator.generate_movie_data({"price": 999999999})
        response = super_admin_movies_api.create_movie(movie_data)
        assert response["price"] == 999999999
        super_admin_movies_api.delete_movie(response["id"])

    # ==================== НЕГАТИВНЫЕ ТЕСТЫ ====================

    def test_create_movie_missing_name(self, super_admin_movies_api):
        """Тест: создание фильма без названия."""
        movie_data = {
            "imageUrl": "https://dummyimage.com/1020x260",
            "price": 928,
            "description": "Test description",
            "location": DataGenerator.get_valid_location(),
            "published": False,
            "genreId": DataGenerator.get_valid_genre_id()
        }

        with pytest.raises(ValueError) as excinfo:
            super_admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value)

    def test_create_movie_missing_price(self, super_admin_movies_api):
        """Негативный тест: создание без обязательного поля price."""
        movie_data = DataGenerator.generate_movie_data()
        del movie_data["price"]

        with pytest.raises(ValueError) as excinfo:
            super_admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value)

    def test_create_movie_missing_description(self, super_admin_movies_api):
        """Негативный тест: создание без поля description."""
        movie_data = DataGenerator.generate_movie_data()
        del movie_data["description"]

        with pytest.raises(ValueError) as excinfo:
            super_admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value)

    def test_create_movie_missing_location(self, super_admin_movies_api):
        """Негативный тест: создание без обязательного поля location."""
        movie_data = DataGenerator.generate_movie_data()
        del movie_data["location"]

        with pytest.raises(ValueError) as excinfo:
            super_admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value)

    def test_create_movie_missing_published(self, super_admin_movies_api):
        """Негативный тест: создание без обязательного поля published."""
        movie_data = DataGenerator.generate_movie_data()
        del movie_data["published"]

        with pytest.raises(ValueError) as excinfo:
            super_admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value)

    def test_create_movie_missing_genre_id(self, super_admin_movies_api):
        """Негативный тест: создание без обязательного поля genreId."""
        movie_data = DataGenerator.generate_movie_data()
        del movie_data["genreId"]

        with pytest.raises(ValueError) as excinfo:
            super_admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value)

    def test_create_movie_empty_data(self, super_admin_movies_api):
        """Негативный тест: создание с пустыми данными."""
        with pytest.raises(ValueError) as excinfo:
            super_admin_movies_api.create_movie({})

        assert "400" in str(excinfo.value)

    def test_create_movie_empty_name(self, super_admin_movies_api):
        """Негативный тест: создание с пустым названием."""
        movie_data = DataGenerator.generate_movie_data({"name": ""})

        with pytest.raises(ValueError) as excinfo:
            super_admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value)

    def test_create_movie_invalid_location(self, super_admin_movies_api):
        """Негативный тест: создание с невалидной локацией."""
        movie_data = DataGenerator.generate_movie_data({"location": "INVALID_CITY"})

        with pytest.raises(ValueError) as excinfo:
            super_admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value)

    def test_create_movie_empty_location(self, super_admin_movies_api):
        """Негативный тест: создание с пустой локацией."""
        movie_data = DataGenerator.generate_movie_data({"location": ""})

        with pytest.raises(ValueError) as excinfo:
            super_admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value)

    def test_create_movie_invalid_genre(self, super_admin_movies_api):
        """Негативный тест: создание с несуществующим жанром."""
        movie_data = DataGenerator.generate_movie_data({"genreId": 99999})

        with pytest.raises(ValueError) as excinfo:
            super_admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value)

    def test_create_movie_invalid_genre_zero(self, super_admin_movies_api):
        """Негативный тест: genreId = 0."""
        movie_data = DataGenerator.generate_movie_data({"genreId": 0})

        with pytest.raises(ValueError) as excinfo:
            super_admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value)

    def test_create_movie_invalid_genre_negative(self, super_admin_movies_api):
        """Негативный тест: отрицательный genreId."""
        movie_data = DataGenerator.generate_movie_data({"genreId": -1})

        with pytest.raises(ValueError) as excinfo:
            super_admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value)

    def test_create_movie_invalid_image_url(self, super_admin_movies_api):
        """Негативный тест: создание с невалидным URL."""
        movie_data = DataGenerator.generate_movie_data({"imageUrl": "not_a_valid_url"})

        with pytest.raises(ValueError) as excinfo:
            super_admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value)

    def test_create_movie_invalid_published_type(self, super_admin_movies_api):
        """Негативный тест: создание с невалидным типом published."""
        movie_data = DataGenerator.generate_movie_data({"published": "not_boolean"})

        with pytest.raises(ValueError) as excinfo:
            super_admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value)

    def test_create_movie_price_as_string(self, super_admin_movies_api):
        """Негативный тест: цена в виде строки."""
        movie_data = DataGenerator.generate_movie_data()
        movie_data["price"] = "not_a_number"

        with pytest.raises(ValueError) as excinfo:
            super_admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value)

    def test_create_movie_duplicate_name(self, super_admin_movies_api):
        """Негативный тест: создание с дублирующимся названием."""
        unique_name = DataGenerator.generate_unique_movie_name()
        movie_data1 = DataGenerator.generate_movie_data({"name": unique_name})
        response1 = super_admin_movies_api.create_movie(movie_data1)
        movie_id1 = response1["id"]

        movie_data2 = DataGenerator.generate_movie_data({"name": unique_name})

        with pytest.raises(ValueError) as excinfo:
            super_admin_movies_api.create_movie(movie_data2)

        assert "409" in str(excinfo.value)

        super_admin_movies_api.delete_movie(movie_id1)

    def test_create_movie_very_long_name(self, super_admin_movies_api):
        """Негативный тест: создание с очень длинным названием."""
        long_name = DataGenerator.generate_long_text(1000)
        movie_data = DataGenerator.generate_movie_data({"name": long_name})

        with pytest.raises(ValueError) as excinfo:
            super_admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value) or "409" in str(excinfo.value)

    def test_create_movie_null_name(self, super_admin_movies_api):
        """Негативный тест: name = null."""
        movie_data = DataGenerator.generate_movie_data()
        movie_data["name"] = None

        with pytest.raises(ValueError) as excinfo:
            super_admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value)

    def test_create_movie_extra_fields(self, super_admin_movies_api):
        """Негативный тест: API отклоняет запрос с неизвестными полями."""
        movie_data = DataGenerator.generate_movie_data()
        movie_data["extraField"] = "should_be_ignored"

        with pytest.raises(ValueError) as excinfo:
            super_admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value)

    def test_create_movie_with_user_role_forbidden(self, common_user):
        """Негативный тест: у пользователя с ролью USER нет прав на создание фильма."""
        movie_data = DataGenerator.generate_movie_data()

        # ✅ Не проверяем статус в send_request
        response_data = common_user.api.movies_api.create_movie(movie_data, expected_status=None)

        # Проверяем ответ вручную
        assert response_data.get("statusCode") == 403
        assert "message" in response_data
        assert "Forbidden" in response_data.get("message", "")

    @pytest.mark.slow
    def test_create_movie_with_user_role_admin(self, admin):
        """
        Негативный тест: у пользователя с ролью ADMIN нет прав на создание фильма.
        Ожидается 403 Forbidden.
        """
        movie_data = DataGenerator.generate_movie_data()

        # ✅ ПРАВИЛЬНО: не проверяем статус в send_request
        response_data = admin.api.movies_api.create_movie(movie_data, expected_status=None)

        # Проверяем ответ вручную
        assert response_data.get("statusCode") == 403
        assert "message" in response_data
        assert "Forbidden" in response_data.get("message", "")