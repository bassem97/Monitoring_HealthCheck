from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from Config.config import Config

class WebDriver:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--ignore-certificate-errors") # Ignore certificate errors
        self.options.add_argument("--allow-insecure-localhost") # Allow self-signed certificates
        self.options.add_argument("--no-sandbox")
        # self.options.add_argument("--headless")  # Uncomment for pipeline

        # Initialize the Service
        self.service = Service(Config.CHROMEDRIVER_PATH)

        # Initialize the WebDriver
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

    def get_driver(self):
        return self.driver

    def quit(self):
        self.driver.quit()