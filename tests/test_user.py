
import pytest
from pydantic import ValidationError

from models.base_models import TestUser

from models.base_models import RegisterUserResponse


class TestUserAPI:

    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data)
        created_user = RegisterUserResponse(**response.json())

        assert created_user.email == creation_user_data.email
        assert created_user.fullName == creation_user_data.fullName
        assert created_user.roles == creation_user_data.roles
        assert created_user.verified is True

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
        response_by_id = super_admin.api.user_api.get_user(created_user_response['id']).json()
        response_by_email = super_admin.api.user_api.get_user(creation_user_data.email).json()

        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        assert response_by_id.get('id') and response_by_id['id'] != '', "ID должен быть не пустым"
        assert response_by_id.get('email') == creation_user_data.email
        assert response_by_id.get('fullName') == creation_user_data.fullName
        expected_roles = [role.value for role in creation_user_data.roles]
        assert response_by_id.get('roles', []) == expected_roles, "Роли не совпадают"
        assert response_by_id.get('verified') is True

    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user(common_user.email, expected_status=403)

    @pytest.mark.slow
    def test_get_user_by_id_admin(self, admin):
        response = admin.api.user_api.get_user(admin.email, expected_status=200)
        assert response.status_code == 200

def test_user_model_rejects_invalid_email():
    with pytest.raises(ValidationError):
        TestUser(email="не-почта", fullName="Иван", password="12345678",
                passwordRepeat="12345678")