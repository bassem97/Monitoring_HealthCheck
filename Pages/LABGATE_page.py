import logging
import time

from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from Pages.base_page import BasePage
from Config.config import Config
from selenium.webdriver.support import expected_conditions as EC
from Locators.locators import LOCATORS #import the LOCATOR object.

# Custom exception for LABGATE operations
class LABGATEError(Exception):
    """Exception raised for errors in LABGATE operations."""
    pass

class LABGATEPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)


    def open_page(self):
        max_attempts = 3

        for attempt in range(1, max_attempts + 1):
            try:
                self.driver.get(Config.LABGATE_URL)
                self.wait.until(EC.presence_of_element_located(LOCATORS.LABGATE_Page.LOGIN_FORM))
                self.logger.info("LABGATE Page opened successfully!")
                return

            except Exception as e:
                if attempt < max_attempts:
                    self.logger.warning(
                        f"Attempt {attempt} to open LABGATE page failed: {e!r}. Retrying..."
                    )
                    time.sleep(2)
                else:
                    error_msg = f"Failed to open LABGATE page after {max_attempts} attempts."
                    self.email_failure_notification("LABGATE page", Config.LABGATE_URL, error_msg)
                    self.logger.error(error_msg)
                    raise LABGATEError(error_msg)


    def login(self):
        try:
            self.find_element(*LOCATORS.LABGATE_Page.USERNAME).send_keys(Config.LABGATE_USERNAME)
            self.find_element(*LOCATORS.LABGATE_Page.PASSWORD).send_keys(Config.PASSWORD)
            self.click_element(*LOCATORS.LABGATE_Page.LOGIN_BUTTON)
            self.click_element(*LOCATORS.LABGATE_Page.DETECT_CITRIX_BUTTON)
            self.accept_confirmation_alert()
            self.wait.until(EC.presence_of_element_located(LOCATORS.LABGATE_Page.SUCCESS_INDICATOR))
            self.logger.info("LABGATE Login successful!")
        except Exception as e:
            error_msg = f"Failed to login to LABGATE"
            self.email_failure_notification("LABGATE Page", Config.LABGATE_URL, error_msg)
            self.logger.error(error_msg)
            raise LABGATEError(error_msg)

    def logout(self):
        try:
            self.click_element(*LOCATORS.LABGATE_Page.SETTINGS_BUTTON)
            self.click_element(*LOCATORS.LABGATE_Page.LOGOUT_LINK)
            self.wait.until(EC.presence_of_element_located(LOCATORS.LABGATE_Page.LOGOFF_SUCCESS_INDICATOR))
            self.email_success_notification("LABGATE website", Config.LABGATE_URL)
            self.logger.info("LABGATE Logout successful!")
        except Exception as e:
            error_msg = f"Failed to logout from LABGATE"
            self.email_failure_notification("LABGATE Page", Config.LABGATE_URL, error_msg)
            self.logger.error(error_msg)
            raise LABGATEError(error_msg)