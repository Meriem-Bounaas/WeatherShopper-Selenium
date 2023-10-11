import pytest
from selenium.webdriver.edge.webdriver import WebDriver
from src.pages.cart_page import CartPage

from src.pages.current_temperature_page import CurrentTemperaturePage
from src.pages.confirmation_page import ConfirmationPage

@pytest.mark.ok
@pytest.mark.parametrize('data', [("test@test.com", "5555555555554444", "1224", "123", "38000")])
def test_end_to_end_ok(browser: WebDriver, data, current_temperature_page: CurrentTemperaturePage, cart_page: CartPage, confirmation_page: ConfirmationPage):
    shop_page = current_temperature_page.do_task()
    shop_page.do_task()
    cart_page.do_task(*data)
    assert confirmation_page.verify_success()
