import logging
import smtplib
import time
from email.mime.text import MIMEText
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from pynput.keyboard import Key, Controller

from Config.email_config import EmailConfig

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.logger = logging.getLogger(__name__)
        self._smtp_connection = None  # To reuse SMTP connection (optional optimization)

        # Use EmailConfig for email settings
        self.email_sender = EmailConfig.EMAIL_SENDER
        self.email_password = EmailConfig.EMAIL_PASSWORD
        self.smtp_server = EmailConfig.SMTP_SERVER
        self.smtp_port = int(EmailConfig.SMTP_PORT) if EmailConfig.SMTP_PORT else 587
        self.success_email_receivers = EmailConfig.SUCCESS_EMAIL_RECEIVERS
        self.failure_email_receivers = EmailConfig.FAILURE_EMAIL_RECEIVERS

    def _send_email(self, subject: str, body: str, recipients: list) -> None:
        """Reusable method to send email with optimized SMTP handling to multiple recipients."""
        msg = MIMEText(body, 'html')
        msg['Subject'] = subject
        msg['From'] = "No-Reply-LabGateLab-HealthCheck"

        try:
            if not self._smtp_connection:
                self.logger.info(f"Connecting to {self.smtp_server}:{self.smtp_port}")
                self._smtp_connection = smtplib.SMTP(self.smtp_server, self.smtp_port)
                self._smtp_connection.starttls()
                self._smtp_connection.login(self.email_sender, self.email_password)
                self.logger.info("SMTP connection established and authenticated.")

            self.logger.info(f"Sending email to {len(recipients)} recipients...")
            for recipient in recipients:
                msg['To'] = recipient
                self._smtp_connection.sendmail(self.email_sender, recipient, msg.as_string())
                self.logger.info(f"Email sent successfully to {recipient}")
            self.logger.info("All emails sent successfully.")
        except smtplib.SMTPAuthenticationError as auth_error:
            self.logger.error(f"SMTP Authentication Error: {auth_error}")
            self._close_smtp_connection()
            raise
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            self._close_smtp_connection()
            raise

    def _close_smtp_connection(self) -> None:
        """Safely close the SMTP connection if it exists."""
        if self._smtp_connection:
            try:
                self._smtp_connection.quit()
                self.logger.info("SMTP connection closed.")
            except Exception as e:
                self.logger.warning(f"Error closing SMTP connection: {e}")
            finally:
                self._smtp_connection = None

    def email_success_notification(self, website_name: str, url: str) -> None:
        """Send a success email notification to all success recipients."""
        body = f"""
        <html>
            <body>
                <p>Dear All,</p>
                <p>{website_name} <a href="{url}">{url}</a> is accessible and it is working fine.</p>
                <p>Danke Gruss / Thanks & Regards</p>
                <p>NGTestlab Application HealthCheck-Up Team</p>
                <p>******<b>This is an auto-generated email, please do not reply.******</b></p>
                <p>For any queries on this Automated Health Check-Up, please contact:</p>
            </body>
        </html>
        """
        self._send_email(
            subject=f"Application Health Check Notification Alert : {website_name} - Success",
            body=body,
            recipients=self.success_email_receivers
        )

    def email_failure_notification(self, website_name: str, url: str, error_message: str) -> None:
        """Send a failure email notification to all failure recipients."""
        body = f"""
        <html>
            <body>
                <p>Dear All,</p>
                <p>{website_name} <a href="{url}">{url}</a> is not accessible.</p>
                <p>Error Message: <div style="color: red;">{error_message}</div></p>
                <p>Danke Gruss / Thanks & Regards</p>
                <p>NGTestlab Application HealthCheck-Up Team</p>
                <p>******<b>This is an auto-generated email, please do not reply.******</b></p>
                <p>For any queries on this Automated Health Check-Up, please contact:</p>
            </body>
        </html>
        """
        self._send_email(
            subject=f"Application Health Check Notification Alert : {website_name} - Failure",
            body=body,
            recipients=self.failure_email_receivers
        )

    def find_element(self, by, value):
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def is_element_present(self, by, value):
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
            self.wait.until(EC.invisibility_of_element_located((by, value)))
            return True
        except Exception as e:
            print(f"Element did not disappear: {e}")
            return False

    def accept_confirmation_alert(self):
        time.sleep(1)
        keyboard = Controller()

        try:
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
            time.sleep(0.5)

            keyboard.press(Key.space)
            keyboard.release(Key.space)
            time.sleep(0.5)

            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
            time.sleep(0.5)

            keyboard.press(Key.enter)
            keyboard.release(Key.enter)

            time.sleep(1)

        except Exception as e:
            self.logger.error(f"Error handling protocol dialog: {e}")
            raise

    def prompt_alert(self, username, password):
        time.sleep(1)
        keyboard = Controller()

        try:
            keyboard.type(username)
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
            time.sleep(0.5)

            keyboard.type(password)
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
            time.sleep(0.5)

            keyboard.press(Key.tab)
            keyboard.release(Key.tab)

            keyboard.press(Key.space)
            keyboard.release(Key.space)

        except Exception as e:
            self.logger.error(f"Error handling protocol dialog: {e}")
            raise