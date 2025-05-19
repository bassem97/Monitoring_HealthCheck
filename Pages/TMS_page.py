import logging
import time

from selenium.webdriver import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from Pages.base_page import BasePage
from Config.config import Config
from selenium.webdriver.support import expected_conditions as EC
from Locators.locators import LOCATORS #import the LOCATOR object.

# Custom exception for TMS operations
class TMSError(Exception):
    """Exception raised for errors in TMS operations."""
    pass

class TMSPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)


    def open_page(self):
        try:
            self.driver.get(Config.TMS_URL)
            self.prompt_alert(Config.TMS_COMMON_USERNAME, Config.TMS_COMMON_PASSWORD)
            self.wait.until(EC.presence_of_element_located(LOCATORS.TMS_Page.LOGIN_FORM))
            self.logger.info("TMS Page opened successfully!")
            self.email_success_notification("TMS", Config.TMS_URL)
        except Exception as e:
            error_msg = f"Failed to open TMS page"
            self.email_failure_notification("TMS Page", Config.TMS_URL, error_msg)
            self.logger.error(error_msg)
            raise TMSError(error_msg)

    def login(self):
        try:
            self.find_element(*LOCATORS.TMS_Page.USERNAME).send_keys(Config.TMS_USERNAME)
            self.find_element(*LOCATORS.TMS_Page.PASSWORD).send_keys(Config.PASSWORD)
            self.find_element(*LOCATORS.TMS_Page.REPOSITORY).send_keys(Config.TMS_REPOSITORY)
            self.click_element(*LOCATORS.TMS_Page.LOGIN_BUTTON)
            self.wait.until(EC.presence_of_element_located(LOCATORS.TMS_Page.SUCCESS_INDICATOR))
            time.sleep(1)
            self.logger.info("TMS Login successful!")
        except Exception as e:
            error_msg = f"Failed to login to TMS"
            self.email_failure_notification("TMS Page", Config.TMS_URL, error_msg)
            self.logger.error(error_msg)
            raise TMSError(error_msg)

    def logout(self):
        try:
            time.sleep(1)
            self.click_element(*LOCATORS.TMS_Page.LOGOUT_BUTTON)
            self.wait.until(EC.presence_of_element_located(LOCATORS.TMS_Page.LOGIN_FORM))
            self.email_success_notification("TMS website", Config.TMS_URL)
            self.logger.info("TMS Logout successful!")
        except Exception as e:
            error_msg = f"Failed to logout from TMS"
            self.email_failure_notification("TMS Page", Config.TMS_URL, error_msg)
            self.logger.error(error_msg)
            raise TMSError(error_msg)