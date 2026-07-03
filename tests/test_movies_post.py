"""
Тесты для POST /movies - Создание фильма
"""
import pytest
from core.data_generator import DataGenerator


class TestMoviesPost:
    """Тесты для POST /movies - Создание фильма."""

    # ==================== ПОЗИТИВНЫЕ ТЕСТЫ ====================

    def test_create_movie_success(self, admin_movies_api):
        """Позитивный тест: успешное создание фильма."""
        movie_data = DataGenerator.generate_movie_data()
        response = admin_movies_api.create_movie(movie_data)

        assert "id" in response
        assert response["name"] == movie_data["name"]
        assert response["description"] == movie_data["description"]
        # Цена округляется до целого числа
        assert response["price"] == int(movie_data["price"])
        assert response["location"] == movie_data["location"]
        assert response["published"] == movie_data["published"]
        assert response["genreId"] == movie_data["genreId"]
        assert "createdAt" in response
        assert "genre" in response

        movie_id = response["id"]
        get_response = admin_movies_api.get_movie_by_id(movie_id)
        assert get_response["id"] == movie_id

        admin_movies_api.delete_movie(movie_id)

    def test_create_movie_with_custom_data(self, admin_movies_api):
        """Позитивный тест: создание фильма с кастомными значениями."""
        custom_data = {
            "name": f"Custom Movie {DataGenerator.generate_string(5)}",
            "price": 500,
            "location": "MSK",
            "published": True,
            "genreId": 2
        }
        movie_data = DataGenerator.generate_movie_data(custom_data)
        response = admin_movies_api.create_movie(movie_data)

        assert response["name"] == custom_data["name"]
        assert response["price"] == custom_data["price"]
        assert response["location"] == custom_data["location"]
        assert response["published"] == custom_data["published"]
        assert response["genreId"] == custom_data["genreId"]

        admin_movies_api.delete_movie(response["id"])

    def test_create_movie_with_all_fields(self, admin_movies_api):
        """Позитивный тест: создание со всеми полями."""
        movie_data = {
            "name": f"Full Movie {DataGenerator.generate_string(6)}",
            "imageUrl": "https://example.com/poster.jpg",
            "price": 350,
            "description": f"Full description {DataGenerator.generate_string(20)}",
            "location": "SPB",
            "published": True,
            "genreId": 3
        }

        response = admin_movies_api.create_movie(movie_data)
        movie_id = response["id"]

        assert response["name"] == movie_data["name"]
        assert response["imageUrl"] == movie_data["imageUrl"]
        assert response["price"] == movie_data["price"]
        assert response["description"] == movie_data["description"]
        assert response["location"] == movie_data["location"]
        assert response["published"] == movie_data["published"]
        assert response["genreId"] == movie_data["genreId"]
        assert response["rating"] is not None

        admin_movies_api.delete_movie(movie_id)

    def test_create_movie_with_different_locations(self, admin_movies_api):
        """Позитивный тест: создание фильмов в разных локациях."""
        for location in ["MSK", "SPB"]:
            movie_data = DataGenerator.generate_movie_data({"location": location})
            response = admin_movies_api.create_movie(movie_data)
            movie_id = response["id"]

            assert response["location"] == location
            admin_movies_api.delete_movie(movie_id)

    def test_create_movie_with_different_published_status(self, admin_movies_api):
        """Позитивный тест: создание с разными статусами публикации."""
        for published_status in [True, False]:
            movie_data = DataGenerator.generate_movie_data({"published": published_status})
            response = admin_movies_api.create_movie(movie_data)
            movie_id = response["id"]

            assert response["published"] == published_status
            admin_movies_api.delete_movie(movie_id)

    def test_create_movie_special_characters(self, admin_movies_api):
        """Позитивный тест: создание с названием, содержащим спецсимволы."""
        special_name = DataGenerator.generate_special_characters_string()
        movie_data = DataGenerator.generate_movie_data({"name": special_name})
        response = admin_movies_api.create_movie(movie_data)
        movie_id = response["id"]

        assert response["name"] == special_name
        admin_movies_api.delete_movie(movie_id)

    def test_create_movie_missing_image_url(self, admin_movies_api):
        """
        Проверка: создание без imageUrl (API допускает null).
        """
        movie_data = DataGenerator.generate_movie_data()
        del movie_data["imageUrl"]

        response = admin_movies_api.create_movie(movie_data)
        assert "id" in response
        assert response["imageUrl"] is None

        admin_movies_api.delete_movie(response["id"])

    def test_create_movie_negative_price(self, admin_movies_api):
        """
        Проверка: создание с отрицательной ценой (API допускает).
        """
        movie_data = DataGenerator.generate_movie_data({"price": -100})
        response = admin_movies_api.create_movie(movie_data)

        assert "id" in response
        assert response["price"] == -100

        admin_movies_api.delete_movie(response["id"])

    def test_create_movie_zero_price(self, admin_movies_api):
        """
        Проверка: создание с нулевой ценой (API допускает).
        """
        movie_data = DataGenerator.generate_movie_data({"price": 0})
        response = admin_movies_api.create_movie(movie_data)

        assert "id" in response
        assert response["price"] == 0

        admin_movies_api.delete_movie(response["id"])

    def test_create_movie_empty_description(self, admin_movies_api):
        """
        Проверка: создание с пустым описанием (API допускает).
        """
        movie_data = DataGenerator.generate_movie_data({"description": ""})
        response = admin_movies_api.create_movie(movie_data)

        assert "id" in response
        assert response["description"] == ""

        admin_movies_api.delete_movie(response["id"])

    def test_create_movie_very_large_price(self, admin_movies_api):
        """Граничное значение: очень большая цена."""
        movie_data = DataGenerator.generate_movie_data({"price": 999999999})
        response = admin_movies_api.create_movie(movie_data)
        assert response["price"] == 999999999
        admin_movies_api.delete_movie(response["id"])

    # ==================== НЕГАТИВНЫЕ ТЕСТЫ ====================

    def test_create_movie_missing_name(self, admin_movies_api):
        """Негативный тест: создание без обязательного поля name."""
        movie_data = DataGenerator.generate_movie_data()
        del movie_data["name"]

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value) or "422" in str(excinfo.value)

    def test_create_movie_missing_price(self, admin_movies_api):
        """Негативный тест: создание без обязательного поля price."""
        movie_data = DataGenerator.generate_movie_data()
        del movie_data["price"]

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value) or "422" in str(excinfo.value)

    def test_create_movie_missing_description(self, admin_movies_api):
        """Негативный тест: создание без поля description."""
        movie_data = DataGenerator.generate_movie_data()
        del movie_data["description"]

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value) or "422" in str(excinfo.value)

    def test_create_movie_missing_location(self, admin_movies_api):
        """Негативный тест: создание без обязательного поля location."""
        movie_data = DataGenerator.generate_movie_data()
        del movie_data["location"]

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value) or "422" in str(excinfo.value)

    def test_create_movie_missing_published(self, admin_movies_api):
        """Негативный тест: создание без обязательного поля published."""
        movie_data = DataGenerator.generate_movie_data()
        del movie_data["published"]

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value) or "422" in str(excinfo.value)

    def test_create_movie_missing_genre_id(self, admin_movies_api):
        """Негативный тест: создание без обязательного поля genreId."""
        movie_data = DataGenerator.generate_movie_data()
        del movie_data["genreId"]

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value) or "422" in str(excinfo.value)

    def test_create_movie_empty_data(self, admin_movies_api):
        """Негативный тест: создание с пустыми данными."""
        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.create_movie({})

        assert "400" in str(excinfo.value) or "422" in str(excinfo.value)

    def test_create_movie_empty_name(self, admin_movies_api):
        """Негативный тест: создание с пустым названием."""
        movie_data = DataGenerator.generate_movie_data({"name": ""})

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value) or "422" in str(excinfo.value)

    def test_create_movie_invalid_location(self, admin_movies_api):
        """Негативный тест: создание с невалидной локацией."""
        movie_data = DataGenerator.generate_movie_data({"location": "INVALID_CITY"})

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value) or "422" in str(excinfo.value)

    def test_create_movie_empty_location(self, admin_movies_api):
        """Негативный тест: создание с пустой локацией."""
        movie_data = DataGenerator.generate_movie_data({"location": ""})

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value) or "422" in str(excinfo.value)

    def test_create_movie_invalid_genre(self, admin_movies_api):
        """Негативный тест: создание с несуществующим жанром."""
        movie_data = DataGenerator.generate_movie_data({"genreId": 99999})

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value) or "404" in str(excinfo.value)

    def test_create_movie_invalid_genre_zero(self, admin_movies_api):
        """Негативный тест: genreId = 0."""
        movie_data = DataGenerator.generate_movie_data({"genreId": 0})

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value)

    def test_create_movie_invalid_genre_negative(self, admin_movies_api):
        """Негативный тест: отрицательный genreId."""
        movie_data = DataGenerator.generate_movie_data({"genreId": -1})

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value)

    def test_create_movie_invalid_image_url(self, admin_movies_api):
        """Негативный тест: создание с невалидным URL."""
        movie_data = DataGenerator.generate_movie_data({"imageUrl": "not_a_valid_url"})

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value) or "422" in str(excinfo.value)

    def test_create_movie_invalid_published_type(self, admin_movies_api):
        """Негативный тест: создание с невалидным типом published."""
        movie_data = DataGenerator.generate_movie_data({"published": "not_boolean"})

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value) or "422" in str(excinfo.value)

    def test_create_movie_price_as_string(self, admin_movies_api):
        """Негативный тест: цена в виде строки."""
        movie_data = DataGenerator.generate_movie_data()
        movie_data["price"] = "not_a_number"

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value) or "422" in str(excinfo.value)

    def test_create_movie_duplicate_name(self, admin_movies_api):
        """Негативный тест: создание с дублирующимся названием."""
        unique_name = DataGenerator.generate_unique_movie_name()
        movie_data1 = DataGenerator.generate_movie_data({"name": unique_name})
        response1 = admin_movies_api.create_movie(movie_data1)
        movie_id1 = response1["id"]

        movie_data2 = DataGenerator.generate_movie_data({"name": unique_name})

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.create_movie(movie_data2)

        assert "409" in str(excinfo.value)

        admin_movies_api.delete_movie(movie_id1)

    def test_create_movie_very_long_name(self, admin_movies_api):
        """Негативный тест: создание с очень длинным названием."""
        long_name = DataGenerator.generate_long_text(1000)
        movie_data = DataGenerator.generate_movie_data({"name": long_name})

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value) or "409" in str(excinfo.value)

    def test_create_movie_null_name(self, admin_movies_api):
        """Негативный тест: name = null."""
        movie_data = DataGenerator.generate_movie_data()
        movie_data["name"] = None

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value) or "422" in str(excinfo.value)

    def test_create_movie_extra_fields(self, admin_movies_api):
        """Негативный тест: API отклоняет запрос с неизвестными полями."""
        movie_data = DataGenerator.generate_movie_data()
        movie_data["extraField"] = "should_be_ignored"

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.create_movie(movie_data)

        assert "400" in str(excinfo.value)