from src.pages.base.base_page import BasePage
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.common.by import By

from src.utils.common import send_by_chunk, wait_click, wait_new_url


class CartPage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.driver = driver

        self.url = 'https://weathershopper.pythonanywhere.com/cart'
        self.title = 'Cart Items'
        self.header = 'Checkout'

    locators = {
        'header_elm': ("XPATH", "//h2"),
        'total_elem': ("XPATH", "//*[@id='total']"),
        'payment_iframe': ("XPATH", "//iframe[@name='stripe_checkout_app']"),
        'pay_with_card_btn': ("CSS", ".stripe-button-el")
    }

    def go_to_page(self) -> None:
        self.driver.get(self.url)

    def verify_total_prices_shop(self) -> None:
        item_prices = self.driver.find_elements(
            By.XPATH, "/html/body/div[1]/div[2]/table/tbody/tr/td[2]")

        total_prices = sum([int(price.text) for price in item_prices])
        return total_prices == int(self.total_elem.text.split(' ')[-1])

    def payment(self, email: str, card_number: str, card_expires: str, card_CVV: str, zip_code: str) -> None:
        # Switch frame
        wait_click(self.driver, self.pay_with_card_btn)
        self.driver.switch_to.frame(self.payment_iframe)

        # Locate frame elements
        payment_email_input = self.driver.find_element(
            By.CSS_SELECTOR, "#email")
        card_number_input = self.driver.find_element(
            By.XPATH, "//input[@placeholder='Numéro de carte']")
        card_expires_input = self.driver.find_element(
            By.XPATH, "//input[@placeholder='MM / AA']")
        card_CVV_input = self.driver.find_element(
            By.XPATH, "//input[@placeholder='CVV']")
        submit_payment_btn = self.driver.find_element(
            By.CSS_SELECTOR, "#submitButton")

        # Enter values to inputs
        payment_email_input.send_keys(email)
        send_by_chunk(card_number_input, card_number, 4)
        send_by_chunk(card_expires_input, card_expires, 2)
        card_CVV_input.send_keys(card_CVV)

        if card_number != '':
            # Zip Code is showing only now
            zip_code_input = self.driver.find_element(
                By.XPATH, "//input[@placeholder='ZIP Code' or @placeholder='CP']")
            zip_code_input.send_keys(zip_code)

        # Submit
        wait_click(self.driver, submit_payment_btn)

    def do_task(self, email: str, card_number: str, card_expires: str, card_CVV: str, zip_code: str) -> None:
        self.payment(email, card_number, card_expires, card_CVV, zip_code)
        self.driver.switch_to.default_content()
        wait_new_url(self.driver, self.url)

    def do_task_error(self, email: str, card_number: str, card_expires: str, card_CVV: str, zip_code: str) -> None:
        self.payment(email, card_number, card_expires, card_CVV, zip_code)

    def verify_fail(self, invalid_inputs_name: list[str]) -> bool:
        payment_email_input = self.driver.find_element(
            By.CSS_SELECTOR, "#email")
        card_number_input = self.driver.find_element(
            By.XPATH, "//input[@placeholder='Numéro de carte']")
        card_expires_input = self.driver.find_element(
            By.XPATH, "//input[@placeholder='MM / AA']")
        card_CVV_input = self.driver.find_element(
            By.XPATH, "//input[@placeholder='CVV']")
        zip_code_input = self.driver.find_element(
            By.XPATH, "//input[@autocompletetype='postal-code']")
        submit_payment_btn = self.driver.find_element(
            By.CSS_SELECTOR, "#submitButton")

        wait_click(self.driver, submit_payment_btn)

        inputs = [payment_email_input, card_number_input,
                  card_expires_input, card_CVV_input, zip_code_input]

        # Check if 'invalid' is in the class attribute of every invalid inputs
        invalid_inputs = list(filter(lambda x: f'{x=}'.split('=')[
                              0] in invalid_inputs_name, inputs))
        res = ['invalid' in input.getAttribute(
            "class") for input in invalid_inputs]
        return all(res)

    def verify_page(self) -> bool:
        return super().verify_page(self.url, self.title, self.header_elm, self.header)
