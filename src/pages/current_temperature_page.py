from src.pages.base.base_page import BasePage
from selenium.webdriver.edge.webdriver import WebDriver

from src.pages.moisturizers_page import MoisturizersPage
from src.pages.sunscreens_page import SunscreensPage
from src.utils.common import wait_click


class CurrentTemperaturePage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.driver = driver

        self.url = 'https://weathershopper.pythonanywhere.com/'
        self.title = 'Current Temperature'
        self.header = 'Current temperature'

    locators = {
        'header_elm': ("XPATH", "//h2"),
        'temperature': ("ID", "temperature"),
        'sunscreens': ("XPATH", "//a[@href='/sunscreen']"),
        'moisturizers': ("XPATH", "//a[@href='/moisturizer']")
    }

    def do_task(self) -> MoisturizersPage | SunscreensPage:
        temperature = int(self.temperature.text.split(' ')[0])

        if temperature < 19:
            wait_click(self.driver, self.moisturizers)
            return MoisturizersPage(self.driver)
        
        if temperature > 34:
            wait_click(self.driver, self.sunscreens)
            return SunscreensPage(self.driver)

    def verify_page(self) -> bool:
        return super().verify_page(self.url, self.title, self.header_elm, self.header)
