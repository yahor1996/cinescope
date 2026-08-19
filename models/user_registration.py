from pydantic import BaseModel
from conftest import registration_user_data

class User(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str
    roles: list[str]

# Для себя тест на проверку данных юзера через BaseModel
def test_validate_user_data(registration_user_data):
    user = User(**registration_user_data)