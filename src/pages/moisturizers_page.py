from src.pages.base.base_page import BasePage
from selenium.webdriver.edge.webdriver import WebDriver

from src.utils.common import find_least_expensive_item_by_name, wait_click


class MoisturizersPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.driver = driver

        self.url = 'https://weathershopper.pythonanywhere.com/moisturizer'
        self.title = 'The Best Moisturizers in the World!'
        self.header = 'Moisturizers'

    locators = {
        'header_elm': ("XPATH", "//h2"),
        'cart_btn': ("XPATH", "//button[@onclick='goToCart()']")
    }

    def go_to_page(self) -> None:
        self.driver.get(self.url)

    def do_task(self) -> None:
        least_price_btn = find_least_expensive_item_by_name(self.driver, 'Aloe')
        wait_click(self.driver, least_price_btn)
        least_price_btn = find_least_expensive_item_by_name(self.driver, 'almond')
        wait_click(self.driver, least_price_btn)

        wait_click(self.driver, self.cart_btn)

    def verify_page(self) -> bool:
        return super().verify_page(self.url, self.title, self.header_elm, self.header)

        
