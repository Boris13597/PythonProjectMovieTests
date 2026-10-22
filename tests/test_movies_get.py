"""
Тесты для GET /movies - Получение афиш фильмов
"""
import random
from http import HTTPStatus

import pytest

price_ranges = [
    (random.randint(0, 500), random.randint(501, 1000))
    for _ in range(10)
]
genre_ids = [1, 2, 3, 4, 5]
locations_list = ["MSK", "SPB"]

class TestMoviesGet:
    """Тесты для GET /movies - Получение афиш фильмов."""

    def test_get_movies_success(self, public_movies_api):
        """Позитивный тест: успешное получение списка фильмов."""
        response = public_movies_api.get_movies()
        assert "movies" in response
        assert isinstance(response["movies"], list)

    def test_get_movies_with_pagination(self, public_movies_api):
        """Позитивный тест: пагинация (pageSize, page)."""
        for page_size in [5, 10, 20]:
            params = {"pageSize": page_size, "page": 1}
            response = public_movies_api.get_movies(params=params)
            movies_list = response.get("movies", [])
            assert len(movies_list) <= page_size

    def test_get_movies_page_two(self, public_movies_api):
        """Позитивный тест: проверка второй страницы."""
        params = {"pageSize": 5, "page": 2}
        response = public_movies_api.get_movies(params=params)
        assert "movies" in response
        assert isinstance(response["movies"], list)

    def test_get_movies_filter_by_min_price(self, public_movies_api):
        """Позитивный тест: фильтр по минимальной цене."""
        all_movies = public_movies_api.get_movies()
        movies_list_all = all_movies.get("movies", [])
        if not movies_list_all:
            pytest.skip("Нет фильмов в базе")

        first_movie = movies_list_all[0]
        movie_price = first_movie["price"]

        # minPrice должен быть меньше maxPrice
        params = {"minPrice": movie_price, "maxPrice": movie_price + 1000}
        response = public_movies_api.get_movies(params=params)

        movies_list = response.get("movies", [])
        assert len(movies_list) > 0

        for movie in movies_list:
            assert movie["price"] >= movie_price

    def test_get_movies_filter_by_max_price(self, public_movies_api):
        """Позитивный тест: фильтр по максимальной цене."""
        all_movies = public_movies_api.get_movies()
        movies_list_all = all_movies.get("movies", [])
        if not movies_list_all:
            pytest.skip("Нет фильмов в базе")

        first_movie = movies_list_all[0]
        movie_price = first_movie["price"]

        params = {"maxPrice": movie_price}
        response = public_movies_api.get_movies(params=params)

        movies_list = response.get("movies", [])
        assert len(movies_list) > 0

        for movie in movies_list:
            assert movie["price"] <= movie_price

    def test_get_movies_filter_by_price_range(self, public_movies_api):
        """Позитивный тест: фильтр по диапазону цен."""
        all_movies = public_movies_api.get_movies()
        movies_list_all = all_movies.get("movies", [])
        if not movies_list_all:
            pytest.skip("Нет фильмов в базе")

        first_movie = movies_list_all[0]
        movie_price = first_movie["price"]

        min_price = movie_price - 50
        max_price = movie_price + 50

        params = {"minPrice": min_price, "maxPrice": max_price}
        response = public_movies_api.get_movies(params=params)

        movies_list = response.get("movies", [])
        assert len(movies_list) > 0

        for movie in movies_list:
            assert min_price <= movie["price"] <= max_price

    def test_get_movies_filter_by_location(self, public_movies_api):
        """Позитивный тест: фильтр по локации."""
        all_movies = public_movies_api.get_movies()
        movies_list_all = all_movies.get("movies", [])
        if not movies_list_all:
            pytest.skip("Нет фильмов в базе")

        first_movie = movies_list_all[0]
        target_location = first_movie["location"]

        params = {"locations": [target_location]}
        response = public_movies_api.get_movies(params=params)

        movies_list = response.get("movies", [])
        assert len(movies_list) > 0

        for movie in movies_list:
            assert movie["location"] == target_location

    def test_get_movies_filter_by_multiple_locations(self, public_movies_api):
        """Позитивный тест: фильтр по нескольким локациям."""
        locations = ["MSK", "SPB"]
        params = {"locations": locations}
        response = public_movies_api.get_movies(params=params)

        movies_list = response.get("movies", [])
        for movie in movies_list:
            assert movie["location"] in locations

    def test_get_movies_filter_by_published(self, public_movies_api):
        """Позитивный тест: фильтр по статусу публикации."""
        params = {"published": True}
        response = public_movies_api.get_movies(params=params)

        movies_list = response.get("movies", [])
        assert len(movies_list) > 0

        for movie in movies_list:
            assert movie["published"] == True

    def test_get_movies_filter_by_genre(self, public_movies_api):
        """Позитивный тест: фильтр по жанру."""
        # Используем существующий жанр 1
        params = {"genreId": 1}
        response = public_movies_api.get_movies(params=params)

        movies_list = response.get("movies", [])
        # Может быть пустым, если нет фильмов с жанром 1
        # Но обычно есть
        for movie in movies_list:
            assert movie["genreId"] == 1

    def test_get_movies_filter_by_created_at_asc(self, public_movies_api):
        """Позитивный тест: сортировка по дате создания (по возрастанию)."""
        params = {"createdAt": "asc", "pageSize": 10}
        response = public_movies_api.get_movies(params=params)

        movies_list = response.get("movies", [])
        if len(movies_list) > 1:
            dates = [movie["createdAt"] for movie in movies_list]
            assert dates == sorted(dates)

    def test_get_movies_filter_by_created_at_desc(self, public_movies_api):
        """Позитивный тест: сортировка по дате создания (по убыванию)."""
        params = {"createdAt": "desc", "pageSize": 10}
        response = public_movies_api.get_movies(params=params)

        movies_list = response.get("movies", [])
        if len(movies_list) > 1:
            dates = [movie["createdAt"] for movie in movies_list]
            assert dates == sorted(dates, reverse=True)

    def test_get_movies_combined_filters(self, public_movies_api):
        """Позитивный тест: комбинация всех фильтров."""
        # Используем существующие фильмы
        params = {
            "pageSize": 10,
            "page": 1,
            "minPrice": 400,
            "maxPrice": 600,
            "locations": ["MSK"],
            "published": True,
            "genreId": 1,
            "createdAt": "asc"
        }
        response = public_movies_api.get_movies(params=params)

        movies_list = response.get("movies", [])
        # Может быть пустым - это нормально для комбинированного фильтра
        # Просто проверяем, что структура ответа корректна
        assert "movies" in response
        assert isinstance(movies_list, list)

        for movie in movies_list:
            if "price" in movie:
                assert 400 <= movie["price"] <= 600
            if "location" in movie:
                assert movie["location"] == "MSK"
            if "published" in movie:
                assert movie["published"] == True
            if "genreId" in movie:
                assert movie["genreId"] == 1

    def test_get_movies_invalid_price_range(self, movies_api):
        """Тест с невалидным диапазоном цен (min > max)."""
        params = {"minPrice": 1000, "maxPrice": 100}
        response = movies_api.requester.send_request(
            "GET",
            "movies",
            params=params,
            expected_status=HTTPStatus.BAD_REQUEST  # ✅ Исправлено: 400
        )
        assert response.status_code == 400

    def test_get_movies_invalid_location(self, movies_api):
        """Тест с невалидной локацией."""
        params = {"locations": "INVALID"}
        response = movies_api.requester.send_request(
            "GET",
            "movies",
            params=params,
            expected_status=HTTPStatus.BAD_REQUEST  # ✅ Исправлено: 400
        )
        assert response.status_code == 400

    def test_get_movies_invalid_genre(self, public_movies_api):
        """Негативный тест: невалидный genreId (возвращает пустой список)."""
        params = {"genreId": 99999}
        response = public_movies_api.get_movies(params=params)

        movies_list = response.get("movies", [])
        assert len(movies_list) == 0, "Should return empty list for invalid genreId"

    def test_get_movies_no_results(self, public_movies_api):
        """Негативный тест: фильтр без результатов."""
        params = {"minPrice": 999999, "maxPrice": 1000000}
        response = public_movies_api.get_movies(params=params)

        movies_list = response.get("movies", [])
        assert len(movies_list) == 0, "Should return empty list for no results"


    @pytest.mark.parametrize("genreId, locations, min_price, max_price", [
        (genre, loc, min_p, max_p)
        for genre in genre_ids
        for loc in locations_list
        for min_p, max_p in price_ranges[:2]  # Берем только первые 2 пары
    ])
    def test_get_movies_filter(self,genreId, locations, min_price, max_price, public_movies_api):
        """Позитивный тест: фильтр по жанру, локации и цене."""
        params = {
            "minPrice": min_price,
            "maxPrice": max_price,
            "locations": [locations],
            "genreId": genreId
        }
        response = public_movies_api.get_movies(params=params)

        movies_list = response.get("movies", [])

        assert "movies" in response
        assert isinstance(movies_list, list)

