from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from models.base_models import BaseModelForbid


class Location(str, Enum):
    MSK = "MSK"
    SPB = "SPB"

# --- самые внутренние модели ---

class Genre(BaseModelForbid):
    """Жанр внутри фильма. Приходит как {"name": "Драма"}."""
    name: str
    id: Optional[int] = None

class ReviewUser(BaseModelForbid):
    """Автор отзыва. Приходит как {"fullName": "Melissa Ellis"}."""
    fullName: str

# --- средний уровень ---

class Review(BaseModelForbid):
    userId: str
    text: str
    rating: int = Field(..., ge=0, le=5)
    createdAt: datetime
    user: ReviewUser            # вложенная модель

class Movie(BaseModelForbid):
    id: int = Field(strict=True)
    name: str
    description: str
    genreId: int
    imageUrl: str
    price: int
    rating: float = Field(..., ge=0, le=5)
    location: Location
    published: bool
    createdAt: datetime
    genre: Genre              # вложенная модель

# --- то, что реально возвращают эндпоинты ---

class MoviesPage(BaseModelForbid):
    """Ответ GET /movies - страница со списком фильмов."""
    movies: list[Movie]         # список вложенных моделей
    count: int
    page: int
    pageSize: int
    pageCount: int

class MovieDetails(Movie):
    """Ответ GET /movies/{id} - тот же фильм, но ещё и с отзывами.

    Наследуемся от Movie, чтобы не переписывать 11 полей заново.
    """
    reviews: list[Review]

class BaseModelForbid(BaseModel):
    model_config = ConfigDict(extra="forbid")

