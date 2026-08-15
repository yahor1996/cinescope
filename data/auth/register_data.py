from utils.data_generator import DataGenerator

def get_register_payload(roles=None):
    password = DataGenerator.generate_valid_password()
    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": f"{DataGenerator.generate_firstname()} {DataGenerator.generate_lastname()}",
        "password": password,
        "passwordRepeat": password,
        "roles": roles or ["USER"]
    }