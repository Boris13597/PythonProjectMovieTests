"""Песочница. Запуск: python -m sandbox.playground"""
import sys

from pydantic import ConfigDict, ValidationError

from models.base_models import TestUser, logger, get_user
from sandbox import payloads
from sandbox.models import Movie, MovieDetails, MoviesPage

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def title(text):
    print(f"\n{'=' * 15} {text} {'=' * 15}")


title("1. Один вызов разбирает всё дерево")
page = MoviesPage(**payloads.MOVIES_PAGE)

print("тип page.movies         :", type(page.movies).__name__)
print("тип page.movies[0]      :", type(page.movies[0]).__name__)
print("тип page.movies[0].genre:", type(page.movies[0].genre).__name__)
print("доступ через точку      :", page.movies[0].genre.name)
print("id жанра                :", page.movies[0].genre.id)

title("2. Три уровня вложенности")
details = MovieDetails(**payloads.MOVIE_DETAILS)

print("фильм               :", details.name)
print("жанр (уровень2)     :", details.genre.name)
print("автор отзыва (ур. 3):", details.reviews[0].user.fullName)
print("createdAR стал      :", type(details.createdAt).__name__)
print("location стал       :", repr(details.location))

title("3. Ошибка внутри вложенной модели")
try:
    MoviesPage(**payloads.BROKEN_TYPES)
except ValidationError as e:
    print(e)
    print("\nloc-кортежи:")
    for err in e.errors():
        print("   ", err["loc"], "->", err["type"])

title("4. Поломка на третьем уровне")
try:
    MovieDetails(**payloads.BROKEN_DEEP)
except ValidationError as e:
    for err in e.errors():
        print("   ", ".".join(str(p) for p in err["loc"]), "->", err["msg"])

title("5. Пропала вложенная модель")
try:
    MoviesPage(**payloads.MISSING_NESTED)
except ValidationError as e:
    for err in e.errors():
        print("   ", err["loc"], "->", err["msg"])

title("6. Жанр второго фильма ")
print(f"Название жанра второго фильма {page.movies[1].genre.name}")


title("Практика 6.1. TestUser без verified и banned")
testuser = TestUser(**get_user())
logger.info(f"{testuser.email=} {testuser.fullName=} {testuser.password=} {testuser.passwordRepeat=} {testuser.roles=}")

print(testuser.model_dump_json())
print(testuser.model_dump_json(exclude_unset=True))
print(testuser.model_dump_json(exclude_none=True))

title("7. extra: что делать с лишними полями")

print("-- ignore (по умолчанию) --")
try:
    p_ignore = MoviesPage(**payloads.WITH_EXTRA_FIELDS)
    print("   объект создался, totalRevenue доступен?", hasattr(p_ignore, "totalRevenue"))
except ValidationError as e:
    print("MoviesPage запрещает лишние поля (extra='forbid')")
    for err in e.errors():
        print("      ", err["loc"], "->", err["msg"])


class MoviesPageAllow(MoviesPage):
    model_config = ConfigDict(extra="allow")


print("-- allow --")
try:
    p_allow = MoviesPageAllow(**payloads.WITH_EXTRA_FIELDS)
    print("   model_extra          :", p_allow.model_extra)
    print("   доступ .totalRevenue :", p_allow.totalRevenue)
except ValidationError as e:
    print("Вложенная Movie всё ещё запрещает лишние поля")
    for err in e.errors():
        print("      ", err["loc"], "->", err["msg"])


class MoviesPageForbid(MoviesPage):
    model_config = ConfigDict(extra="forbid")


print("-- forbid --")
try:
    MoviesPageForbid(**payloads.WITH_EXTRA_FIELDS)
except ValidationError as e:
    for err in e.errors():
        print("   ", err["loc"], "->", err["msg"])

title("8. strict: запрещаем приведение типов")

class StrictMovie(Movie):
    model_config = ConfigDict(strict=True)

sample = dict(payloads.MOVIES_PAGE["movies"][0])
sample["price"] = "130"

print("--lax--")
print("  price ->", Movie(**sample).price, type(Movie(**sample).price).__name__)

print("-- strict --")
try:
    StrictMovie(**sample)
except ValidationError as e:
    for err in e.errors():
        print("   ", err["loc"], "->", err["msg"])

title("Практика 8.1. Валидация паролей и email")

print("--одинаковые пароли--")
try:
    user_ok = TestUser(
        email="test@example.com",
        fullName="Test User",
        password="secret123",
        passwordRepeat="secret123",
        roles=["USER"],
    )
    print("Объект создан:", user_ok.email)
except ValidationError as e:
    print("Ошибка")
    for err in e.errors():
        print("   ", err["loc"], "->", err["msg"])

try:
    TestUser(
        email="test@example.com",
        fullName="Test User",
        password="secret123",
        passwordRepeat="different456",
        roles=["USER"],
    )
except ValidationError as e:
    print(e)
    print("\nДетали ошибок:")
    for err in e.errors():
        print("   loc:", err["loc"])
        print("   msg:", err["msg"])
        print("   type:", err["type"])

print("-- неверный email --")
try:
    TestUser(
        email="не-почта",
        fullName="Test User",
        password="secret123",
        passwordRepeat="secret123",
        roles=["USER"],
    )
except ValidationError as e:
    for err in e.errors():
        print("   loc:", err["loc"])
        print("   msg:", err["msg"])

