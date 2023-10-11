from typing import Iterator

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from src.pages.cart_page import CartPage

from src.pages.confirmation_page import ConfirmationPage
from src.pages.current_temperature_page import CurrentTemperaturePage
from src.pages.moisturizers_page import MoisturizersPage
from src.pages.sunscreens_page import SunscreensPage


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call) -> None:
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        if 'browser' in item.fixturenames:
            web_driver = item.funcargs['browser']
        else:
            print('Failed to find web driver')
            return

        # Attach a screenshot if a test failed
        allure.attach(
            web_driver.get_screenshot_as_png(),
            name='screenshot',
            attachment_type=allure.attachment_type.PNG
        )


def pytest_addoption(parser) -> None:
    parser.addoption(
        "--browser-type", action="store", default="edge", help="options: chrome, edge, firefox"
    )


@pytest.fixture(scope='package')
def browser_type(request) -> str:
    return request.config.getoption("--browser-type")


@pytest.fixture()
def browser(browser_type: str, request) -> Iterator[WebDriver]:
    # SetUpClass
    if browser_type == 'chrome':
        driver = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager().install()))
    elif browser_type == 'firefox':
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()))
    else:
        driver = webdriver.Edge(service=EdgeService(
            EdgeChromiumDriverManager().install()))

    driver.implicitly_wait(5)
    driver.get('https://weathershopper.pythonanywhere.com/')
    driver.maximize_window()

    yield driver

    # TearDownClass
    driver.quit()


@pytest.fixture()
def current_temperature_page(browser: WebDriver) -> CurrentTemperaturePage:
    current_temperature = CurrentTemperaturePage(browser)
    yield current_temperature


@pytest.fixture()
def confirmation_page(browser: WebDriver) -> ConfirmationPage:
    confirmation = ConfirmationPage(browser)
    yield confirmation


@pytest.fixture()
def moisturizers_page(browser: WebDriver) -> MoisturizersPage:
    moisturizers = MoisturizersPage(browser)
    yield moisturizers


@pytest.fixture()
def sunscreens_page(browser: WebDriver) -> SunscreensPage:
    sunscreens = SunscreensPage(browser)
    yield sunscreens


@pytest.fixture()
def cart_page(browser: WebDriver) -> CartPage:
    cart = CartPage(browser)
    yield cart
