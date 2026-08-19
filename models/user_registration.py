from pydantic import BaseModel
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
