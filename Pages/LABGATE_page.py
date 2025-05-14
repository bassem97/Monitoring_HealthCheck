import logging

from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from Pages.base_page import BasePage
from Config.config import Config
from selenium.webdriver.support import expected_conditions as EC
from Locators.locators import LOCATORS #import the LOCATOR object.

class LABGATEPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)

    def login(self):
        try:
            self.driver.get(Config.LABGATE_URL)
            self.find_element(*LOCATORS.LABGATE_Page.USERNAME).send_keys(Config.LABGATE_USERNAME)
            self.find_element(*LOCATORS.LABGATE_Page.PASSWORD).send_keys(Config.PASSWORD)
            self.click_element(*LOCATORS.LABGATE_Page.LOGIN_BUTTON)
            self.click_element(*LOCATORS.LABGATE_Page.DETECT_CITRIX_BUTTON)

            self.accept_confirmation_alert()

            self.wait.until(EC.presence_of_element_located(LOCATORS.LABGATE_Page.SUCCESS_INDICATOR))
            self.logger.info("TRT Login successful!")
        except Exception as e:
            self.logger.error(f"Error during TRT login: {e}")
            raise

    def logout(self):
        try:
            self.click_element(*LOCATORS.TRT_Page.LOGOUT_LINK)
            self.wait.until(EC.presence_of_element_located(LOCATORS.TRT_Page.LOGIN_FORM))
            self.logger.info("TRT Logout successful!")
        except Exception as e:
            self.logger.error(f"Error during TRT logout: {e}")
            raise