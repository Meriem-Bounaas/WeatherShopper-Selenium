from seleniumpagefactory.Pagefactory import PageFactory
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class BasePage(PageFactory):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__()
        self.driver = driver

    locators = {
    }

    def verify_url(self, url: str) -> bool:
        return self.driver.current_url == url

    def verify_title(self, title: str) -> bool:
        return self.driver.title == title

    def verify_header(self, header_elm: WebElement, header: str) -> bool:
        return header_elm.text == header

    def verify_page(self, url: str, title: str, header_elm: WebElement, header: str) -> bool:
        return self.verify_url(url) and self.verify_title(title) and self.verify_header(header_elm, header)