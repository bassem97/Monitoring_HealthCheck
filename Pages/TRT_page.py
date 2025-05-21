import logging
import time

from Pages.base_page import BasePage
from Config.config import Config
from selenium.webdriver.support import expected_conditions as EC
from Locators.locators import LOCATORS #import the LOCATOR object.

# Custom exception for TRT operations
class TRTError(Exception):
    """Exception raised for errors in TRT operations."""
    pass

class TRTPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)

    def open_page(self):
        max_attempts = 3

        for attempt in range(1, max_attempts + 1):
            try:
                self.driver.get(Config.TRT_URL)
                self.wait.until(EC.presence_of_element_located(LOCATORS.TRT_Page.LOGIN_FORM))
                self.logger.info(f"TRT page opened successfully on attempt {attempt}.")
                return

            except Exception as e:
                if attempt < max_attempts:
                    self.logger.warning(
                        f"Attempt {attempt} to open TRT page failed: {e!r}. Retrying..."
                    )
                    time.sleep(2)
                else:
                    error_msg = f"Failed to open TRT page after {max_attempts} attempts."
                    self.email_failure_notification("TRT Page", Config.TRT_URL, error_msg)
                    self.logger.error(error_msg)
                    raise TRTError(error_msg)

    def login(self):
        try:
            self.find_element(*LOCATORS.TRT_Page.USERNAME).send_keys(Config.TRT_USERNAME)
            self.find_element(*LOCATORS.TRT_Page.PASSWORD).send_keys(Config.PASSWORD)
            self.click_element(*LOCATORS.TRT_Page.LOGIN_BUTTON)
            self.wait.until(EC.presence_of_element_located(LOCATORS.TRT_Page.SUCCESS_INDICATOR))
            self.logger.info("TRT Login successful!")
        except Exception as e:
            error_msg = f"Failed to login to TRT page"
            self.email_failure_notification("TRT Page", Config.TRT_URL, error_msg)
            self.logger.error(error_msg)
            raise TRTError(error_msg)

    def logout(self):
        try:
            self.click_element(*LOCATORS.TRT_Page.LOGOUT_LINK)
            self.wait.until(EC.presence_of_element_located(LOCATORS.TRT_Page.LOGIN_FORM))
            self.email_success_notification("TRT website", Config.TRT_URL)
            self.logger.info("TRT Logout successful!")
        except Exception as e:
            error_msg = f"Failed to logout from TRT"
            self.email_failure_notification("TRT Page", Config.TRT_URL, error_msg)
            self.logger.error(error_msg)
            raise TRTError(error_msg)