import logging
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator
from core.data_generator import DataGenerator
from constans.roles import Roles


EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

logger = logging.getLogger(__name__)

class TestUser(BaseModel):
    """Тело запроса на создание пользователя (POST /register и POST /user)."""

    id: Optional[str] = None
    email: str = Field(..., pattern=EMAIL_PATTERN, description="Email пользователя")
    fullName: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8, max_length=20)
    passwordRepeat: str = Field(..., min_length=8, max_length=20)
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        """passwordRepeat обязан совпадать с password."""
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("passwordRepeat не совпадает с password")
        return value

class RegisterUserResponse(BaseModel):
    """Ответ на POST /register и POST /user."""

    id: Optional[str] = None
    email: str = Field(..., pattern=EMAIL_PATTERN)
    fullName: str = Field(..., min_length=1, max_length=100)
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    createdAt: datetime
    banned: Optional[bool] = None

def get_user():
    random_password = DataGenerator.generate_random_password()
    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value]
    }

def test_user_data():
    user = TestUser(**get_user())
    logger.info(f"{user.email=} {user.fullName=} {user.password=} {user.passwordRepeat=} {user.roles=}")

class BaseModelForbid(BaseModel):
    model_config = ConfigDict(extra="forbid")
