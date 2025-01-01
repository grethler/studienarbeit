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
    b = Browser(logger, settings)
    d = b.browser
    d.get(settings["urls"]["NZZ"])
    # login
    d.find_element(By.CLASS_NAME, "fup-login").click()
    sleep(10)
    iframe = d.find_element(By.XPATH, "/html/body/div[3]/div/iframe")
    d.switch_to.frame(iframe)
    path = '//*[@id="autofill-form"]/screen-login/p['
    d.find_element(By.XPATH, path+'3]/input').send_keys(settings["email"])
    d.find_element(By.XPATH, path+'4]/input').send_keys(settings["password"])
    d.find_element(By.XPATH, path+'6]/button').click()
    sleep(2000)
    d.quit()

if __name__ == "__main__":
    logger = create_logger()
    with open("settings.yml", "r") as file:
        settings = yaml.safe_load(file)
    get_nzz(logger, settings)
