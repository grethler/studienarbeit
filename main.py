#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Authors: Florian Grethler <grethlef@dhbw-loerrach.de>
#          Ronald Wagner <wagnerr@dhbw-loerrach.de>

import logging
import yaml
from time import sleep
from selenium.webdriver.common.by import By
from src.browser import Browser



def create_logger():
    logformatter = logging.Formatter(' %(name)s :: %(levelname)-8s :: %(message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    logger.handlers[0].setFormatter(logformatter)
    return logger

def get_nzz(logger, settings):
    browser = Browser(logger, settings)

    # login
    browser.login_nzz()
    browser.searchTask()
    browser.articleIteration()
    sleep(2000)
    browser.browser.quit()

if __name__ == "__main__":
    logger = create_logger()
    with open("settings.yml", "r") as file:
        settings = yaml.safe_load(file)
    get_nzz(logger, settings)
