import pytest
from selenium.webdriver.edge.webdriver import WebDriver

from src.pages.cart_page import CartPage
from src.pages.moisturizers_page import MoisturizersPage
from src.pages.sunscreens_page import SunscreensPage


@pytest.mark.ok
def test_add_sunscreens_to_cart_ok(browser: WebDriver, sunscreens_page: SunscreensPage, cart_page: CartPage) -> None:
    sunscreens_page.go_to_page()
    assert  sunscreens_page.verify_page()
    sunscreens_page.do_task()
    assert cart_page.verify_page()


@pytest.mark.ok
def test_add_moisturizers_to_cart_ok(browser: WebDriver, moisturizers_page: MoisturizersPage, cart_page: CartPage) -> None:
    moisturizers_page.go_to_page()
    assert moisturizers_page.verify_page()
    moisturizers_page.do_task()
    assert cart_page.verify_page()
