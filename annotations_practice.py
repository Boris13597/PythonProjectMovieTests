from typing import Optional, Union, Dict, Any, List
import logging
from pydantic import BaseModel


def multiply(a: int, b: int) -> int:
    return a * b


multiply(3, 2)


def sum_numbers(numbers: List[int]) -> int:
    return sum(numbers)


sum_numbers([1, 2, 3])


def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Пользователь найден"
    return None


result1 = find_user(1)
result2 = find_user(999)

if result1:
    print(f"Результат: {result1}")  # Выведет: Результат: Пользователь найден
else:
    print("Пользователь не найден")

if result2:
    print(f"Результат: {result2}")
else:
    print("Пользователь не найден")  # Выведет это

# Дополнительная проверка типов
print(type(result1))  # <class 'str'>
print(type(result2))  # <class 'NoneType'>


def process_input(value: Union[int, str]) -> str:
    return f"Ты передал {value}"


process_input(4365)


class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Привет, меня зовут {self.name}!"


user = User("Артем", 25)
print(user.greet())

def get_even_numbers(numbers: List[int]):
    return [num for num in numbers if num % 2 == 0]

logger = logging.getLogger(__name__)

class User(BaseModel):
    name: str
    age: int
    adult: bool


def get_user():
    return {
        "name": "Alice",
        "age": 25,
        "adult": "true"
    }

def test_user_date():
    user = User(**get_user())
    assert user.name == "Alice"
    logger.info(f"{user.name=} {user.age=} {user.adult=}")

class PlainUser:
    name: str

u = PlainUser()
u.name = 12345