import logging
import time

from selenium.common import NoAlertPresentException
from selenium.webdriver import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from pynput.keyboard import Key, Controller



class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.logger = logging.getLogger(__name__)


    def find_element(self, by, value):
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def is_element_present(self , by, value):
        """
        Checks if an element is present in the DOM.

        Args:
            by: The locator strategy (e.g. By.ID, By.NAME, By.XPATH, etc.)
            value: The locator value (e.g. 'myId', 'myName', '//div', etc.)

        Returns:
            True if the element is present, False otherwise.
        """
        if self.driver.find_elements(by, value):
            return True
        else:
            return False


    def click_element(self, by, value):
        """
        # Checks if an element is present in the DOM,
          then waits for it to be clickable and clicks it.

        Args:
            by: The locator strategy (e.g. By.ID, By.NAME, By.XPATH, etc.)
            value: The locator value (e.g. 'myId', 'myName', '//div', etc.)

        Returns:
            None
        """
        try:
            # Wait for the element to be present
            element = self.wait.until(EC.presence_of_element_located((by, value)))

            # Wait for the element to be clickable
            element = self.wait.until(EC.element_to_be_clickable((by, value)))

            # Click the element
            element.click()

        except Exception as e:
            print(f"Error clicking element (by={by}, value={value}): {e}")
            raise  # Re-raise the exception to propagate it

    class class_attribute_does_not_contain(object):
        """
        # Custom expected condition to wait until an element's class
          attribute does not contain a specific text.

        Args:
            object: The base class for all classes in Python.

        Returns:
            The element if the class attribute does not contain the text,
            False otherwise.
        """

        def __init__(self, locator, text):
            self.locator = locator
            self.text = text

        def __call__(self, driver):
            element = presence_of_element_located(self.locator)(driver)
            if element:
                classes = element.get_attribute("class")
                if classes and self.text not in classes:
                    return element
                else:
                    return False
            else:
                return False

    def wait_until_class_disappears(self, by, value, class_to_remove, timeout=120):
        """
        Wait until an element's class attribute does not contain a specific text.

        Args:
            by: The locator strategy (e.g. By.ID, By.NAME, By.XPATH, etc.)
            value: The locator value (e.g. 'myId', 'myName', '//div', etc.)
            class_to_remove: The text that should not be present in the class attribute.
            timeout: The maximum time to wait (in seconds). #added docstring.

        Returns:
            The element if the class attribute does not contain the text,
            False otherwise.
        """
        return WebDriverWait(self.driver, timeout).until(
            self.class_attribute_does_not_contain((by, value), class_to_remove))

    def wait_for_element_to_disappear(self, by, value, timeout=40):
        """
        Waits for a specific element to disappear from the DOM.

        Args:
            by: The locator strategy (e.g., By.ID, By.XPATH).
            value: The locator value (e.g., "my-id", "//*[@id='my-id']").
            timeout: The maximum time to wait (in seconds).

        Returns:
            True if the element disappears, False otherwise.
        """
        try:
            self.wait.until(EC.invisibility_of_element_located((by,value)))
            return True
        except Exception as e:
            print(f"Element did not disappear: {e}")
            return False

#  create a function that accept a confirmation alert
    def accept_confirmation_alert(self):
        # Wait for the dialog to appear
        time.sleep(1)

        # Press Tab to focus on "Open xdg-open" button, then Enter to click it
        # For Chrome on Windows/Linux, typically Tab once then Enter works
        keyboard = Controller()

        try:
            # First Tab to focus the checkbox (Tab sequence depends on browser)
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
            time.sleep(0.5)

            # Press Space to check the checkbox
            keyboard.press(Key.space)
            keyboard.release(Key.space)
            time.sleep(0.5)

            # Tab again to move to the "Open xdg-open" button
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
            time.sleep(0.5)
            #
            # Press Enter to click the button
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)

            # Wait for dialog processing
            time.sleep(1)

        except Exception as e:
            self.logger.error(f"Error handling protocol dialog: {e}")
            raise


