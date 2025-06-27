import logging
import os
from dotenv import load_dotenv
import yaml

# Load environment variables
load_dotenv()

# Load email configuration from YAML file
with open(os.path.join(os.path.dirname(__file__), 'email_config.yaml'), 'r') as file:
    email_config = yaml.safe_load(file)

class EmailConfig:
    EMAIL_SENDER = os.getenv("EMAIL_SENDER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = os.getenv("SMTP_PORT")
    SUCCESS_EMAIL_RECEIVERS = email_config.get('success_email_receivers', [])
    FAILURE_EMAIL_RECEIVERS = email_config.get('failure_email_receivers', [])

    @staticmethod
    def validate():
        logger = logging.getLogger(__name__)
        if not EmailConfig.EMAIL_SENDER:
            logger.error("EMAIL_SENDER is not set in the environment variables.")
            raise ValueError("EMAIL_SENDER is not set in the environment variables.")
        # if not EmailConfig.EMAIL_PASSWORD:
        #     logger.error("EMAIL_PASSWORD is not set in the environment variables.")
            raise ValueError("EMAIL_PASSWORD is not set in the environment variables.")
        if not EmailConfig.SMTP_SERVER:
            logger.error("SMTP_SERVER is not set in the environment variables.")
            raise ValueError("SMTP_SERVER is not set in the environment variables.")
        if not EmailConfig.SMTP_PORT:
            logger.error("SMTP_PORT is not set in the environment variables.")
            raise ValueError("SMTP_PORT is not set in the environment variables.")
        if not EmailConfig.SUCCESS_EMAIL_RECEIVERS or any(not email for email in EmailConfig.SUCCESS_EMAIL_RECEIVERS):
            logger.error("SUCCESS_EMAIL_RECEIVERS is not set or contains empty values in the email_config.yaml.")
            raise ValueError("SUCCESS_EMAIL_RECEIVERS must be set and contain at least one valid email address.")
        if not EmailConfig.FAILURE_EMAIL_RECEIVERS or any(not email for email in EmailConfig.FAILURE_EMAIL_RECEIVERS):
            logger.error("FAILURE_EMAIL_RECEIVERS is not set or contains empty values in the email_config.yaml.")
            raise ValueError("FAILURE_EMAIL_RECEIVERS must be set and contain at least one valid email address.")
        logger.info("All email-related environment variables and YAML configurations are set.")