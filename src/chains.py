from src.helpers.webdriver_instance import WebDriver
import time


class Chains(WebDriver):
    def __init__(self, headless=True):
        super().__init__(headless=headless)
        self.base_url = "https://chainlist.org/"

    def _requests(self):
        return [request.url for request in self.driver.requests if request.response]

    def logic(self):
        self.driver.get(self.base_url)
        time.sleep(5)
        page_height = self.driver.execute_script(
            "return Number(document.body.scrollHeight)"
        )
        for i in range(0, page_height, 500):
            self.driver.execute_script(f"window.scrollTo(0, {i} );")
            time.sleep(0.15)
        time.sleep(12)  # Wait for all the responses to arrive
        return [url for url in self._requests() if url.endswith(".json")]
