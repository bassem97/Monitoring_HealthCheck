import logging
import sys
import time

import yaml

from Config.config import Config
from Config.email_config import EmailConfig
from Drivers.driver import WebDriver
from Pages.LABGATE_page import LABGATEPage, LABGATEError
from Pages.TMS_page import TMSPage
from Pages.TRT_page import TRTPage

logger = logging.getLogger(__name__)

def test_auth_flow():
    driver_instance = WebDriver()
    driver = driver_instance.get_driver()

    try:
        Config.validate()
        EmailConfig.validate()

        # Load configuration from YAML
        with open("test_config.yaml", "r") as f:
            config = yaml.safe_load(f)


        # # Perform login & logout on TRT
        TRT_page = TRTPage(driver)
        TRT_page.open_page()
        TRT_page.login()
        TRT_page.logout()

        # # Perform login & logout on Labgate
        # LABGATE_page = LABGATEPage(driver)
        # LABGATE_page.open_page()
        # LABGATE_page.login()
        # LABGATE_page.logout()

        # Perform login & logout on Labgate
        # TMS_page = TMSPage(driver)
        # TMS_page.open_page()
        # TMS_page.login()
        # TMS_page.logout()




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