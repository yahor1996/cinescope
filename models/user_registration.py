from pydantic import BaseModel, field_validator, ValidationError
from typing import Optional
from constants.roles import Roles
from conftest import registration_user_data, test_user

class User(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str
    roles: list[Roles]
    banned: Optional[bool] = None
    verified: Optional[bool] = None

    @field_validator("email")
    def check_email(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("Почта не содержит @")
        return value

    @field_validator("password")
    def check_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Пароль меньше 8 символов")
        return value


# Для себя тест на проверку данных юзера через BaseModel
def test_validate_registration_user_data(registration_user_data):
    User(**registration_user_data)

def test_validate_test_user_data(test_user):
    User(**test_user)

def test_convert_to_json(test_user):
    json_data = User(**test_user).model_dump_json(exclude_unset=True)
    print(json_data)

def test_convert_to_json_negative(creation_user_data):
    json_data = User(**creation_user_data).model_dump_json()
    print(json_data)

def test_email_validator_negative(registration_user_data):
    try:
        registration_user_data["email"] = "kek0qvz3v631gmail.com"
        User(**registration_user_data)
    except ValidationError as e:
        print(f"Ошибка валидации: {e}")

def test_password_validator_negative(registration_user_data):
    try:
        registration_user_data["password"] = "^8+tH#_"
        User(**registration_user_data)
    except ValidationError as e:
        print(f"Ошибка валидации: {e}")
