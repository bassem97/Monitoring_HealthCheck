import yaml
from selenium.webdriver.common.by import By


# Load locators from a YAML file
def load_locators(locator_file):
    try:
        with open(locator_file, "r") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return {}  # Return an empty dictionary in case of error
    except FileNotFoundError:
        print(f"Error: Locator file not found at {locator_file}")
        return {}


class Locators:
    def __init__(self, locator_file="Locators/locators.yaml"):
        self.data = load_locators(locator_file)
        self.create_attributes()

    def create_attributes(self):
        for page_name, page_locators in self.data.items():
            page_obj = type(page_name, (object,), {})
            for locator_name, locator_data in page_locators.items():
                by = getattr(By, locator_data["by"].upper())
                value = locator_data["value"]
                setattr(page_obj, locator_name, (by, value))
            setattr(self, page_name, page_obj)

LOCATORS = Locators()  # Instantiate the Locators object