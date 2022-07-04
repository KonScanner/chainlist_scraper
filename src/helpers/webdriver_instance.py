from src.config import Config
from seleniumwire import webdriver
import time as t
from webdriver_manager.chrome import ChromeDriverManager


class WebDriver:
    def __init__(self, headless=True):
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=Config(headless=headless).options
        )
        self.driver.maximize_window()

    def __exit__(self):
        self.driver.quit()
