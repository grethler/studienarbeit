#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Authors: Florian Grethler <grethlef@dhbw-loerrach.de>
#          Ronald Wagner <wagnerr@dhbw-loerrach.de>

from enum import Enum
import logging
import os
import shutil
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
    sort_articles()
    sleep(2000)
    browser.browser.quit()

def get_month(month):
    match(month):
        case("01"):
            return "Januar"
        case("02"):
            return "Februar"
        case("03"):
            return "März"
        case("04"):
            return "April"
        case("05"):
            return "Mai"
        case("06"):
            return "Juni"
        case("07"):
            return "Juli"
        case("08"):
            return "August"
        case("09"):
            return "September"
        case("10"):
            return "Oktober"
        case("11"):
            return "November"
        case("12"):
            return "Dezember"

def sort_articles():
    download_dir = os.path.abspath("./downloads")
    for i in os.listdir(download_dir):
        splitted = i.split("_")
        date = splitted[len(splitted) - 1].strip(".pdf")
        date = date.split("-")
        year = date[0]
        month = date[1]
        day = date[2]
        if not os.path.exists(f"{download_dir}/{year}"):
            os.makedirs(f"{download_dir}/{year}")
        if not os.path.exists(f"{download_dir}/{year}/{get_month(month)}"):
            os.makedirs(f"{download_dir}/{year}/{get_month(month)}")
        source_file = f"{download_dir}/{i}"
        destination_path = f"{download_dir}/{year}/{get_month(month)}"
        shutil.move(source_file, destination_path)
        

if __name__ == "__main__":
    logger = create_logger()
    with open("settings.yml", "r") as file:
        settings = yaml.safe_load(file)
    get_nzz(logger, settings)
