from playwright.sync_api import Page, expect
from utils.data_generator import DataGenerator
import time

def test_registration(page: Page):
    page.goto('https://dev-cinescope.coconutqa.ru/register')

    username_locator = '[data-qa-id="register_full_name_input"]'
    username_value = f"{DataGenerator.generate_firstname()} {DataGenerator.generate_lastname()}"
    page.fill(username_locator, username_value)

    email_locator = '[data-qa-id="register_email_input"]'
    email_value = DataGenerator.generate_random_email()
    page.fill(email_locator, email_value)

    password_value = DataGenerator.generate_valid_password()
    password_locator = '[data-qa-id="register_password_input"]'
    repeat_password_locator = '[data-qa-id="register_password_repeat_input"]'

    page.fill(password_locator, password_value)
    page.fill(repeat_password_locator, password_value)

    register_button_locator = '[data-qa-id="register_submit_button"]'
    page.click(register_button_locator)

    page.wait_for_url('https://dev-cinescope.coconutqa.ru/login')
    expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(visible=True)

    time.sleep(10)
