import pytest
from selenium.webdriver.edge.webdriver import WebDriver

from src.pages.cart_page import CartPage
from src.pages.confirmation_page import ConfirmationPage


@pytest.mark.ok
@pytest.mark.parametrize('data', [("test@test.com", "5555555555554444", "1224", "123", "38000")])
def test_checkout_ok(browser: WebDriver, data, cart_page: CartPage, confirmation_page: ConfirmationPage):
    cart_page.go_to_page()
    assert cart_page.verify_page()
    assert cart_page.verify_total_prices_shop()

    cart_page.do_task(*data)

    assert confirmation_page.verify_page()
    assert confirmation_page.verify_success()


@pytest.mark.ko
@pytest.mark.parametrize('data, invalid_inputs',
                         [({"email": "", "card_number": "", "card_expires": "", "card_CVV": "", "zip_code": ""}, ["payment_email_input", "card_number_input", "card_expires_input", "card_CVV_input", "zip_code_input"]),
                          ({"email": "test", "card_number": "5555555555554444", "card_expires": "1224", "card_CVV": "123", "zip_code": "38000"}, ["payment_email_input"]),
                          ({"email": "test@test.com", "card_number": "5555555555555555", "card_expires": "1224", "card_CVV": "123", "zip_code": "38000"}, ["card_number_input"]),
                          ({"email": "test@test.com", "card_number": "5555555555554444", "card_expires": "12", "card_CVV": "123", "zip_code": "38000"}, ["card_expires_input"]),
                          ({"email": "test@test.com", "card_number": "5555555555554444", "card_expires": "1224", "card_CVV": "12", "zip_code": "38000"}, ["card_CVV_input"]),
                          ({"email": "test@test.com", "card_number": "5555555555554444", "card_expires": "1224", "card_CVV": "123", "zip_code": ""}, ["zip_code_input"])])
def test_checkout_ko(browser: WebDriver, data, invalid_inputs, cart_page: CartPage):
    cart_page.go_to_page()
    assert cart_page.verify_page()
    # assert cart_page.verify_total_prices_shop()

    cart_page.do_task_error(data["email"], data["card_number"], data["card_expires"], data["card_CVV"], data["zip_code"])

    assert cart_page.verify_fail(invalid_inputs)
