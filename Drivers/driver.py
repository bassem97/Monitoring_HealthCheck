import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from Config.config import Config
from webdriver_manager.chrome import ChromeDriverManager

class WebDriver:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--ignore-certificate-errors")  # Ignore certificate errors
        self.options.add_argument("--allow-insecure-localhost")  # Allow self-signed certificates
        # self.options.add_argument("--headless")  # Uncomment for pipeline

        try:
            driver_path = ChromeDriverManager().install()
            self.service = Service(driver_path)
        except Exception as e:
            print(f"Failed to download ChromeDriver: {e}")
            driver_path = Config.CHROMEDRIVER_PATH
            if not os.path.exists(driver_path):
                raise FileNotFoundError(f"ChromeDriver not found at {driver_path}")
            self.service = Service(driver_path)

        self.driver = webdriver.Chrome(service=self.service, options=self.options)

    def get_driver(self):
        return self.driver

    def quit(self):
        self.driver.quit()