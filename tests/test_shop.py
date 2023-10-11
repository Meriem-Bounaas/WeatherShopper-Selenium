import pytest
from selenium.webdriver.edge.webdriver import WebDriver

from src.pages.current_temperature_page import CurrentTemperaturePage


@pytest.mark.ok
def test_shop_moisturizers_or_sunscreens_ok(browser: WebDriver, current_temperature_page: CurrentTemperaturePage) -> None:
    assert current_temperature_page.verify_page()

    shop_page = current_temperature_page.do_task()
    assert shop_page.verify_page()
