import logging
import sys
import time

import yaml

from Config.config import Config
from Drivers.driver import WebDriver
from Pages.LABGATE_page import LABGATEPage, LABGATEError
from Pages.TRT_page import TRTPage

logger = logging.getLogger(__name__)

def test_auth_flow():
    driver_instance = WebDriver()
    driver = driver_instance.get_driver()

    try:
        Config.validate()  # Ensure credentials are set

        # Load configuration from YAML
        with open("test_config.yaml", "r") as f:
            config = yaml.safe_load(f)


        # Perform login & logout on TRT
        TRT_login_page = TRTPage(driver)
        TRT_login_page.open_page()
        TRT_login_page.login()
        TRT_login_page.logout()

        # # Perform login & logout on Labgate
        # LABGATE_login_page = LABGATEPage(driver)
        # LABGATE_login_page.open_page()
        # LABGATE_login_page.login()
        # LABGATE_login_page.logout()




    except LABGATEError as e:
        # Just print the error message without the stack trace
        print(f"ERROR: {str(e)}")
        sys.exit(1)  # Exit immediately with error code

    except Exception as e:
        # For unexpected errors, show full error
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)  # Exit immediately with error code

    finally:
        if driver_instance:
            time.sleep(2)
            driver_instance.quit()
            logger.info("Test completed")

if __name__ == "__main__":
    test_auth_flow()