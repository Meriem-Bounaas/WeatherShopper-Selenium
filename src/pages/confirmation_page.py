from src.pages.base.base_page import BasePage
from selenium.webdriver.edge.webdriver import WebDriver


class ConfirmationPage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.driver = driver

        self.url = 'https://weathershopper.pythonanywhere.com/confirmation'
        self.title = 'Confirmation'
        self.header = 'PAYMENT SUCCESS'

    locators = {
        'header_elm': ("XPATH", "//h2"),
        'success_elm': ("CSS", ".text-justify")
    }

    def verify_success(self) -> bool:
        return 'Your payment was successful' in self.success_elm.text

    def verify_page(self) -> bool:
        return super().verify_page(self.url, self.title, self.header_elm, self.header)