#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Authors: Florian Grethler <grethlef@dhbw-loerrach.de>
#          Ronald Wagner <wagnerr@dhbw-loerrach.de>

import logging
import os
import argparse
import shutil
import yaml
from time import sleep
from src.browser_nzz import Browser_nzz
from src.browser_handelsblatt import Browser_handelsblatt


def create_logger():
    logformatter = logging.Formatter(' %(name)s :: %(levelname)-8s :: %(message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    logger.handlers[0].setFormatter(logformatter)
    return logger

def get_nzz(logger, settings, cli):
    browser = Browser_nzz(logger, settings, cli)

    # login
    browser.login_nzz()
    browser.searchTask()
    browser.articleIteration()
    #sort_articles("nzz")
    #sleep(2000)
    browser.browser.quit()

def get_handelsblatt(logger, settings, cli):
    browser = Browser_handelsblatt(logger, settings, cli)

    # login
    browser.login_handelsblatt()
    browser.searchTask()
    browser.articleIteration()
    #sort_articles("handelsblatt")
    #sleep(2000)
    browser.browser.quit()

def sort_articles(media):
    download_dir = os.path.abspath(f"./downloads/{media}")
    for i in os.listdir(download_dir):
        splitted = i.split("_")
        date = splitted[len(splitted) - 1].strip(".pdf")
        date = date.split("-")
        year = date[0]
        month = date[1]
        day = date[2]
        if not os.path.exists(f"{download_dir}/{year}"):
            os.makedirs(f"{download_dir}/{year}")
        if not os.path.exists(f"{download_dir}/{year}/{month}"):
            os.makedirs(f"{download_dir}/{year}/{month}")
        source_file = f"{download_dir}/{i}"
        destination_path = f"{download_dir}/{year}/{month}"
        shutil.move(source_file, destination_path)


if __name__ == "__main__":
    logger = create_logger()

    with open("settings.yml", "r") as file:
        settings = yaml.safe_load(file)

    args = argparse.ArgumentParser()
    args.add_argument("-c", "--crawl", action="store_true", help="Crawl the websites")
    args.add_argument("-s", "--sort", action="store_true", help="Sort the articles")
    args.add_argument("-t", "--train", action="store_true", help="Train the model")
    args.add_argument("--cli", action="store_true", help="Use headless mode")
    args = args.parse_args()

    if not any([args.crawl, args.train, args.sort]):
        print("No arguments given. Please use -h to get help.")
        exit(1)

    if sum([args.crawl, args.train, args.sort]) > 1:
        print("Please use only one argument at a time.")
        exit(1)

    if args.crawl:
        get_nzz(logger, settings, args.cli)
        get_handelsblatt(logger, settings, args.cli)

    if args.sort:
        sort_articles("nzz")
        sort_articles("handelsblatt")

    if args.train:
        pass
        #train_model(logger, settings)

    exit(0)
