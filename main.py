import logging
import yaml
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService

def create_logger():
    logformatter = logging.Formatter(' %(name)s :: %(levelname)-8s :: %(message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    logger.handlers[0].setFormatter(logformatter)
    return logger

class Browser:
    def __init__(self, logger, settings):
        opts = Options()
        #opts.add_argument("--headless")
        opts.add_argument("--disable-gpu")
        self.browser = webdriver.Firefox(
            service=FirefoxService(),
            options=opts)
        self.logger = logger
        self.settings = settings


if __name__ == "__main__":
    logger = create_logger()
    with open("settings.yml", "r") as file:
        settings = yaml.safe_load(file)
    b = Browser(logger, settings)
    b.browser.get("https://www.google.com")
    b.browser.quit()
