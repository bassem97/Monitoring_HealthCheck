import logging
import time

import yaml

from Config.config import Config
from Drivers.driver import WebDriver
from Pages.LABGATE_page import LABGATEPage
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
        # TRT_login_page = TRTPage(driver)
        # TRT_login_page.login()
        # TRT_login_page.logout()

        # Perform login & logout on Labgate
        LABGATE_login_page = LABGATEPage(driver)
        LABGATE_login_page.login()

        # # Web Trace Page
        # templates_page = TemplatesPage(driver)
        # templates_page.access_eoSearch_page()
        # templates_page.pick_template(config["template_name"], config["from_time"], config["to_time"])
        # templates_page.filter_template(config["imsi"], config["msisdn"])
        # templates_page.search_template()
        # templates_page.export_template()
        # templates_page.download_template()
        #
        # time.sleep(2)  # Add delay or additional actions here

        # Perform logout
        # logout_page = LogoutPage(driver)
        # logout_page.logout()

    except Exception as e:
       logger.error(f"Error during test: {e}")
    finally:
        time.sleep(2)
        driver_instance.quit()
        logger.info("Test completed")

if __name__ == "__main__":
    test_auth_flow()