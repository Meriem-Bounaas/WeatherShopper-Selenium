from selenium.webdriver.remote.webelement import WebElement
from selenium.common import StaleElementReferenceException
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


def wait_click(driver: WebDriver, element: WebElement) -> None:
    WebDriverWait(driver, 20, ignored_exceptions=[StaleElementReferenceException]).until(
        EC.element_to_be_clickable(element)).click()


def wait_new_url(driver: WebDriver, url: str) -> None:
    WebDriverWait(driver, 20).until(EC.url_changes(url))


def find_least_expensive_item_by_name(driver: WebDriver, name: str):
    selected_prices = driver.find_elements(
        By.XPATH, f"//p[contains(text(), '{name.upper()}') or contains(text(), '{name.lower()}') or contains(text(), '{name.capitalize()}')]/following-sibling::p")
    least_expensive_price = min(
        [int(price.text.split(' ')[-1]) for price in selected_prices])
    return driver.find_element(By.XPATH, f"//button[contains(@onclick, '{least_expensive_price}')]")


def send_by_chunk(input: WebElement, text: str, chunk_size: int):
    for i in range(0, len(text), chunk_size):
        input.send_keys(text[i:i+chunk_size])
