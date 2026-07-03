"""
Тесты для PATCH /movies/{id} - Редактирование фильма
"""
import pytest
from core.data_generator import DataGenerator


class TestMoviesPatch:
    """Тесты для PATCH /movies/{id} - Редактирование фильма."""

    # ==================== ПОЗИТИВНЫЕ ТЕСТЫ ====================

    def test_patch_movie_all_fields(self, admin_movies_api, public_movies_api, created_movie):
        """Позитивный тест: обновление всех полей фильма."""
        movie_id = created_movie

        # Получаем текущие данные через public_movies_api (PUBLIC)
        original = public_movies_api.get_movie_by_id(movie_id)

        update_data = {
            "name": f"Updated All {DataGenerator.generate_string(5)}",
            "description": f"New description {DataGenerator.generate_string(10)}",
            "price": 999.99,
            "location": "SPB" if original["location"] == "MSK" else "MSK",
            "imageUrl": "https://dummyimage.com/1020x260",
            "published": not original["published"],
            "genreId": 5 if original["genreId"] != 5 else 1
        }

        # Обновляем через admin_movies_api (SUPER_ADMIN)
        response = admin_movies_api.patch_movie(movie_id, update_data)

        assert response["id"] == movie_id
        assert response["name"] == update_data["name"]
        assert response["description"] == update_data["description"]
        assert response["price"] == int(update_data["price"])
        assert response["location"] == update_data["location"]
        assert response["imageUrl"] == update_data["imageUrl"]
        assert response["published"] == update_data["published"]
        assert response["genreId"] == update_data["genreId"]

        # Проверяем через public_movies_api (PUBLIC)
        get_response = public_movies_api.get_movie_by_id(movie_id)
        assert get_response["name"] == update_data["name"]
        assert get_response["price"] == int(update_data["price"])
        assert get_response["published"] == update_data["published"]

    def test_patch_movie_single_field_name(self, admin_movies_api, public_movies_api, created_movie):
        """Позитивный тест: обновление только названия."""
        movie_id = created_movie
        new_name = f"New Name {DataGenerator.generate_string(5)}"
        update_data = {"name": new_name}

        # Обновляем через admin_movies_api
        response = admin_movies_api.patch_movie(movie_id, update_data)

        assert response["id"] == movie_id
        assert response["name"] == new_name

        # Проверяем через public_movies_api
        get_response = public_movies_api.get_movie_by_id(movie_id)
        assert get_response["name"] == new_name

    def test_patch_movie_single_field_price(self, admin_movies_api, public_movies_api, created_movie):
        """Позитивный тест: обновление только цены."""
        movie_id = created_movie
        new_price = 777.77
        update_data = {"price": new_price}

        response = admin_movies_api.patch_movie(movie_id, update_data)

        assert response["id"] == movie_id
        assert response["price"] == int(new_price)

        get_response = public_movies_api.get_movie_by_id(movie_id)
        assert get_response["price"] == int(new_price)

    def test_patch_movie_single_field_description(self, admin_movies_api, public_movies_api, created_movie):
        """Позитивный тест: обновление только описания."""
        movie_id = created_movie
        new_description = f"New description {DataGenerator.generate_string(15)}"
        update_data = {"description": new_description}

        response = admin_movies_api.patch_movie(movie_id, update_data)

        assert response["id"] == movie_id
        assert response["description"] == new_description

        get_response = public_movies_api.get_movie_by_id(movie_id)
        assert get_response["description"] == new_description

    def test_patch_movie_single_field_location(self, admin_movies_api, public_movies_api, created_movie):
        """Позитивный тест: обновление только локации."""
        movie_id = created_movie

        original = public_movies_api.get_movie_by_id(movie_id)
        new_location = "SPB" if original["location"] == "MSK" else "MSK"
        update_data = {"location": new_location}

        response = admin_movies_api.patch_movie(movie_id, update_data)

        assert response["id"] == movie_id
        assert response["location"] == new_location

        get_response = public_movies_api.get_movie_by_id(movie_id)
        assert get_response["location"] == new_location

    def test_patch_movie_single_field_published(self, admin_movies_api, public_movies_api, created_movie):
        """Позитивный тест: обновление статуса публикации."""
        movie_id = created_movie

        original = public_movies_api.get_movie_by_id(movie_id)
        new_published = not original["published"]
        update_data = {"published": new_published}

        response = admin_movies_api.patch_movie(movie_id, update_data)

        assert response["id"] == movie_id
        assert response["published"] == new_published

        get_response = public_movies_api.get_movie_by_id(movie_id)
        assert get_response["published"] == new_published

    def test_patch_movie_single_field_genre(self, admin_movies_api, public_movies_api, created_movie):
        """Позитивный тест: обновление только жанра."""
        movie_id = created_movie

        original = public_movies_api.get_movie_by_id(movie_id)
        new_genre_id = 5 if original["genreId"] != 5 else 1
        update_data = {"genreId": new_genre_id}

        response = admin_movies_api.patch_movie(movie_id, update_data)

        assert response["id"] == movie_id
        assert response["genreId"] == new_genre_id
        assert response["genre"]["name"] is not None

        get_response = public_movies_api.get_movie_by_id(movie_id)
        assert get_response["genreId"] == new_genre_id

    def test_patch_movie_single_field_image_url(self, admin_movies_api, public_movies_api, created_movie):
        """Позитивный тест: обновление только URL изображения."""
        movie_id = created_movie
        new_image_url = "https://dummyimage.com/1020x260"
        update_data = {"imageUrl": new_image_url}

        response = admin_movies_api.patch_movie(movie_id, update_data)

        assert response["id"] == movie_id
        assert response["imageUrl"] == new_image_url

        get_response = public_movies_api.get_movie_by_id(movie_id)
        assert get_response["imageUrl"] == new_image_url

    def test_patch_movie_multiple_fields(self, admin_movies_api, public_movies_api, created_movie):
        """Позитивный тест: обновление нескольких полей одновременно."""
        movie_id = created_movie

        update_data = {
            "name": f"Multiple Update {DataGenerator.generate_string(5)}",
            "description": f"Multiple description {DataGenerator.generate_string(10)}",
            "price": 555.55
        }

        response = admin_movies_api.patch_movie(movie_id, update_data)

        assert response["id"] == movie_id
        assert response["name"] == update_data["name"]
        assert response["description"] == update_data["description"]
        assert response["price"] == int(update_data["price"])

        get_response = public_movies_api.get_movie_by_id(movie_id)
        assert get_response["name"] == update_data["name"]
        assert get_response["description"] == update_data["description"]
        assert get_response["price"] == int(update_data["price"])

    def test_patch_movie_no_changes(self, admin_movies_api, public_movies_api, created_movie):
        """Позитивный тест: отправка пустого тела."""
        movie_id = created_movie

        original = public_movies_api.get_movie_by_id(movie_id)
        response = admin_movies_api.patch_movie(movie_id, {})

        assert response["id"] == movie_id
        assert response["name"] == original["name"]
        assert response["description"] == original["description"]
        assert response["price"] == original["price"]
        assert response["location"] == original["location"]
        assert response["published"] == original["published"]
        assert response["genreId"] == original["genreId"]

    def test_patch_movie_verify_unchanged_fields(self, admin_movies_api, public_movies_api, created_movie):
        """Позитивный тест: проверка, что необновленные поля остались без изменений."""
        movie_id = created_movie

        original = public_movies_api.get_movie_by_id(movie_id)

        new_name = f"Name Only {DataGenerator.generate_string(5)}"
        response = admin_movies_api.patch_movie(movie_id, {"name": new_name})

        assert response["id"] == movie_id
        assert response["name"] == new_name
        assert response["description"] == original["description"]
        assert response["price"] == original["price"]
        assert response["location"] == original["location"]
        assert response["published"] == original["published"]
        assert response["genreId"] == original["genreId"]

    def test_patch_movie_float_price(self, admin_movies_api, public_movies_api, created_movie):
        """Позитивный тест: обновление цены с дробным числом."""
        movie_id = created_movie
        float_price = 123.45
        update_data = {"price": float_price}

        response = admin_movies_api.patch_movie(movie_id, update_data)

        assert response["id"] == movie_id
        assert response["price"] == int(float_price)

    def test_patch_movie_very_large_price(self, admin_movies_api, created_movie):
        """Граничное значение: очень большая цена."""
        movie_id = created_movie
        update_data = {"price": 999999999}

        try:
            response = admin_movies_api.patch_movie(movie_id, update_data)
            assert response["price"] == 999999999
        except ValueError as e:
            assert "400" in str(e) or "413" in str(e)

    # ==================== НЕГАТИВНЫЕ ТЕСТЫ ====================

    def test_patch_movie_not_found(self, admin_movies_api):
        """Негативный тест: обновление несуществующего фильма."""
        fake_id = 999999999
        update_data = {"name": "New Name"}

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.patch_movie(fake_id, update_data)

        assert "404" in str(excinfo.value)

    def test_patch_movie_negative_id(self, admin_movies_api):
        """Негативный тест: обновление с отрицательным ID."""
        update_data = {"name": "New Name"}

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.patch_movie(-1, update_data)

        assert "400" in str(excinfo.value) or "404" in str(excinfo.value)

    def test_patch_movie_zero_id(self, admin_movies_api):
        """Негативный тест: обновление с ID = 0."""
        update_data = {"name": "New Name"}

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.patch_movie(0, update_data)

        assert "400" in str(excinfo.value) or "404" in str(excinfo.value)

    def test_patch_movie_string_id(self, admin_movies_api):
        """Негативный тест: обновление с ID в виде строки."""
        update_data = {"name": "New Name"}

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.patch_movie("not_a_number", update_data)

        assert "400" in str(excinfo.value) or "404" in str(excinfo.value)

    def test_patch_movie_empty_id(self, admin_movies_api):
        """Негативный тест: обновление с пустым ID."""
        update_data = {"name": "New Name"}

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.patch_movie("", update_data)

        assert "400" in str(excinfo.value) or "404" in str(excinfo.value)

    def test_patch_movie_invalid_name_empty(self, admin_movies_api, created_movie):
        """Негативный тест: пустое название."""
        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.patch_movie(created_movie, {"name": ""})
        assert "404" in str(excinfo.value) or "400" in str(excinfo.value)

    def test_patch_movie_null_name(self, admin_movies_api, created_movie):
        """Негативный тест: name = null."""
        update_data = {"name": None}
        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.patch_movie(created_movie, update_data)
        assert "400" in str(excinfo.value) or "422" in str(excinfo.value) or "404" in str(excinfo.value)

    def test_patch_movie_invalid_price_negative(self, admin_movies_api, created_movie):
        """Негативный тест: обновление с отрицательной ценой."""
        movie_id = created_movie
        update_data = {"price": -100}

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.patch_movie(movie_id, update_data)

        assert "400" in str(excinfo.value) or "422" in str(excinfo.value)

    def test_patch_movie_invalid_price_zero(self, admin_movies_api, created_movie):
        """Негативный тест: обновление с нулевой ценой."""
        movie_id = created_movie
        update_data = {"price": 0}

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.patch_movie(movie_id, update_data)

        assert "400" in str(excinfo.value) or "422" in str(excinfo.value)

    def test_patch_movie_price_as_string(self, admin_movies_api, created_movie):
        """Негативный тест: цена в виде строки."""
        movie_id = created_movie
        update_data = {"price": "not_a_number"}

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.patch_movie(movie_id, update_data)

        assert "400" in str(excinfo.value) or "422" in str(excinfo.value)

    def test_patch_movie_invalid_location(self, admin_movies_api, created_movie):
        """Негативный тест: обновление с невалидной локацией."""
        movie_id = created_movie
        update_data = {"location": "INVALID_CITY"}

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.patch_movie(movie_id, update_data)

        assert "400" in str(excinfo.value) or "422" in str(excinfo.value)

    def test_patch_movie_empty_location(self, admin_movies_api, created_movie):
        """Негативный тест: пустая локация."""
        movie_id = created_movie
        update_data = {"location": ""}

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.patch_movie(movie_id, update_data)

        assert "400" in str(excinfo.value) or "422" in str(excinfo.value)

    def test_patch_movie_invalid_genre(self, admin_movies_api, created_movie):
        """Негативный тест: обновление с несуществующим жанром."""
        movie_id = created_movie
        update_data = {"genreId": 99999}

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.patch_movie(movie_id, update_data)

        assert "400" in str(excinfo.value) or "404" in str(excinfo.value)

    def test_patch_movie_invalid_genre_zero(self, admin_movies_api, created_movie):
        """Негативный тест: genreId = 0."""
        movie_id = created_movie
        update_data = {"genreId": 0}

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.patch_movie(movie_id, update_data)

        assert "400" in str(excinfo.value)

    def test_patch_movie_invalid_genre_negative(self, admin_movies_api, created_movie):
        """Негативный тест: отрицательный genreId."""
        movie_id = created_movie
        update_data = {"genreId": -1}

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.patch_movie(movie_id, update_data)

        assert "400" in str(excinfo.value)

    def test_patch_movie_invalid_image_url(self, admin_movies_api, created_movie):
        """Негативный тест: обновление с невалидным URL изображения."""
        movie_id = created_movie
        update_data = {"imageUrl": "not_a_valid_url"}

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.patch_movie(movie_id, update_data)

        assert "400" in str(excinfo.value) or "422" in str(excinfo.value)

    def test_patch_movie_invalid_published_type(self, admin_movies_api, created_movie):
        """Негативный тест: обновление с невалидным типом published."""
        movie_id = created_movie
        update_data = {"published": "not_boolean"}

        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.patch_movie(movie_id, update_data)

        assert "400" in str(excinfo.value) or "422" in str(excinfo.value)

    def test_patch_movie_empty_description_allowed(self, admin_movies_api, created_movie):
        """Проверка: API разрешает обновление с пустым описанием."""
        response = admin_movies_api.patch_movie(created_movie, {"description": ""})
        assert response["description"] == ""
        assert response["id"] == created_movie

    def test_patch_movie_very_long_name(self, admin_movies_api, created_movie):
        """Негативный тест: очень длинное название."""
        long_name = DataGenerator.generate_long_text(1000)
        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.patch_movie(created_movie, {"name": long_name})
        assert "404" in str(excinfo.value) or "413" in str(excinfo.value) or "400" in str(excinfo.value)

    def test_patch_movie_extra_fields(self, admin_movies_api, created_movie):
        """Негативный тест: невалидные поля отклоняются (404)."""
        movie_id = created_movie
        update_data = {
            "name": f"Extra Fields {DataGenerator.generate_string(5)}",
            "extraField": "should_be_ignored"
        }
        with pytest.raises(ValueError) as excinfo:
            admin_movies_api.patch_movie(movie_id, update_data)
        assert "400" in str(excinfo.value) or "404" in str(excinfo.value)

    # ==================== ИНТЕГРАЦИОННЫЕ ТЕСТЫ ====================

    def test_patch_movie_full_lifecycle(self, admin_movies_api, public_movies_api):
        """Интеграционный тест: полный цикл с обновлением."""
        movie_data = DataGenerator.generate_movie_data()
        create_response = admin_movies_api.create_movie(movie_data)
        movie_id = create_response["id"]
        original_name = create_response["name"]

        new_name = f"Updated Lifecycle {DataGenerator.generate_string(5)}"
        update_response = admin_movies_api.patch_movie(movie_id, {"name": new_name})
        assert update_response["name"] == new_name

        get_response = public_movies_api.get_movie_by_id(movie_id)
        assert get_response["name"] == new_name
        assert get_response["name"] != original_name

        admin_movies_api.delete_movie(movie_id)

    def test_patch_movie_and_verify_no_data_loss(self, admin_movies_api, public_movies_api, created_movie):
        """Интеграционный тест: проверка, что при обновлении не теряются данные."""
        movie_id = created_movie

        original = public_movies_api.get_movie_by_id(movie_id)

        new_name = f"No Data Loss {DataGenerator.generate_string(5)}"
        admin_movies_api.patch_movie(movie_id, {"name": new_name})

        updated = public_movies_api.get_movie_by_id(movie_id)

        assert updated["id"] == original["id"]
        assert updated["name"] == new_name
        assert updated["description"] == original["description"]
        assert updated["price"] == original["price"]
        assert updated["location"] == original["location"]
        assert updated["published"] == original["published"]
        assert updated["genreId"] == original["genreId"]
        assert updated["imageUrl"] == original["imageUrl"]
        assert updated["createdAt"] == original["createdAt"]
        assert updated["rating"] == original["rating"]

    def test_patch_movie_check_response_structure(self, admin_movies_api, created_movie):
        """Интеграционный тест: проверка структуры ответа PATCH."""
        movie_id = created_movie
        update_data = {"name": f"Structure Check {DataGenerator.generate_string(5)}"}
        response = admin_movies_api.patch_movie(movie_id, update_data)

        expected_fields = [
            "id", "name", "price", "description", "imageUrl",
            "location", "published", "genreId", "genre",
            "createdAt", "rating"
        ]

        for field in expected_fields:
            assert field in response, f"Missing field in PATCH response: {field}"

        assert isinstance(response["id"], int)
        assert isinstance(response["name"], str)
        assert isinstance(response["price"], (int, float))
        assert isinstance(response["published"], bool)
        assert isinstance(response["genreId"], int)
        assert isinstance(response["genre"], dict)
        assert isinstance(response["rating"], (int, float))

    def test_patch_movie_sequential_updates(self, admin_movies_api, public_movies_api, created_movie):
        """Интеграционный тест: последовательные обновления."""
        movie_id = created_movie

        name1 = f"Update 1 {DataGenerator.generate_string(5)}"
        response1 = admin_movies_api.patch_movie(movie_id, {"name": name1})
        assert response1["name"] == name1

        price2 = 888.88
        response2 = admin_movies_api.patch_movie(movie_id, {"price": price2})
        assert response2["name"] == name1
        assert response2["price"] == int(price2)

        desc3 = f"Description after update {DataGenerator.generate_string(10)}"
        response3 = admin_movies_api.patch_movie(movie_id, {"description": desc3})
        assert response3["name"] == name1
        assert response3["price"] == int(price2)
        assert response3["description"] == desc3

        final = public_movies_api.get_movie_by_id(movie_id)
        assert final["name"] == name1
        assert final["price"] == int(price2)
        assert final["description"] == desc3

    def test_patch_movie_check_created_at_unchanged(self, admin_movies_api, public_movies_api, created_movie):
        """Интеграционный тест: проверка, что createdAt не меняется при обновлении."""
        movie_id = created_movie

        original = public_movies_api.get_movie_by_id(movie_id)
        original_created_at = original["createdAt"]

        update_data = {"name": f"Check CreatedAt {DataGenerator.generate_string(5)}"}
        response = admin_movies_api.patch_movie(movie_id, update_data)

        assert response["createdAt"] == original_created_at

        get_response = public_movies_api.get_movie_by_id(movie_id)
        assert get_response["createdAt"] == original_created_at

    def test_patch_movie_verify_reviews_unchanged(self, admin_movies_api, public_movies_api, created_movie):
        """Интеграционный тест: проверка, что отзывы не меняются при обновлении фильма."""
        movie_id = created_movie

        original = public_movies_api.get_movie_by_id(movie_id)
        original_reviews = original.get("reviews", [])

        update_data = {"name": f"Reviews Check {DataGenerator.generate_string(5)}"}
        response = admin_movies_api.patch_movie(movie_id, update_data)

        if "reviews" in response:
            assert len(response["reviews"]) == len(original_reviews)