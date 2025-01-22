#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Authors: Florian Grethler <grethlef@dhbw-loerrach.de>
#          Ronald Wagner <wagnerr@dhbw-loerrach.de>

from time import sleep
from selenium import webdriver
import os
import requests
import datetime
import json
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService


class Browser_nzz:
    def __init__(self, logger, settings):

        download_dir = os.path.abspath("./downloads/nzz")
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            print(f"Directory created: {download_dir}")
        opts = Options()
        opts.add_experimental_option("prefs", {
            "download.default_directory": download_dir,  # Set download folder
            "download.prompt_for_download": False,      # Disable download prompt
            "directory_upgrade": True                   # Automatically overwrite
            })
        #opts.add_argument("--headless")
        opts.add_argument("--disable-gpu")
        self.browser = webdriver.Chrome(
            service=ChromeService(),
            options=opts)
        self.logger = logger
        self.settings = settings

    def get_nzz_token(self):
        url = "https://id-eu.piano.io/id/api/v1/identity/login/token?aid=p8HiOl0Zpe"
        payload = {"password": self.settings["password"], "remember": True,
                "login": self.settings["email"], "loginType": "email"}
        response = requests.post(url, data=json.dumps(payload),
                                headers={"Content-Type": "application/json"})
        token = response.json()
        expires = datetime.datetime.now() + datetime.timedelta(seconds=token.get("expires_in"))
        token["expires"] = expires.timestamp()
        return json.dumps(token)

    def login_nzz(self):
        # get authorization token
        # limit login attemts by saving token in file
        if not os.path.exists("cookie_nzz"):
            token = self.get_nzz_token()
            with open("cookie_nzz", "w") as f:
                f.write(token)
        else:
            with open("cookie_nzz", "r") as f:
                token = json.loads(f.read())
                if datetime.datetime.now().timestamp() > token.get("expires"):
                    token = self.get_nzz_token()
                    with open("cookie_nzz", "w") as f:
                        f.write(token)
                else:
                    token = token.get("access_token")

        #open URL
        self.browser.get(self.settings["urls"]["NZZ"])

        self.browser.add_cookie({"name": "__utp", "value": token, "domain": ".nzz.ch"})
        self.browser.refresh()

        #focus on login form + login
        #self.browser.find_element(By.CLASS_NAME, "fup-login").click()
        #sleep(3000)
        #iframe = self.browser.find_element(By.XPATH, "/html/body/div[3]/div/iframe")
        #self.browser.switch_to.frame(iframe)
        #path='/html/body/app-main/gm-sso-widget/screen-layout/div/div/main/current-screen/form/screen-login/p['
        #self.browser.find_element(By.XPATH, path+'3]/input').send_keys(self.settings["email"])
        #self.browser.find_element(By.XPATH, path+'4]/input').send_keys(self.settings["password"])
        #self.browser.find_element(By.XPATH, path+'6]/button').click()
        #self.browser.switch_to.default_content()
        sleep(3)

    def searchTask(self):
        self.browser.find_element(By.CLASS_NAME, "fup-archive-query-input").send_keys("Migration")
        self.browser.find_element(By.CLASS_NAME, "fup-s-date-start").send_keys("01.01.2014")
        self.browser.find_element(By.CLASS_NAME, "fup-s-date-end").send_keys("31.01.2024")
        path = "/html/body/div[2]/div[1]/div[1]/div[3]/div[1]/div/div[1]/div"
        self.browser.find_element(By.XPATH, path).click()
        sleep(3)


    def articleIteration(self):
        counter = 0
        num = self.browser.find_element(By.CLASS_NAME, "fup-archive-result-hits").text
        number_of_articles = int(num.split(" ")[0].replace(",", ""))
        self.browser.find_element(By.CLASS_NAME, "fup-archive-result-sort").click()
        sleep(1)

        while counter < 3:  # Change to number_of_articles for full run
            try:
                elements = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "fup-archive-result-item-article"))
                )

                for i in elements:
                    actions = ActionChains(self.browser)
                    actions.move_to_element(i).perform()
                    actions.click(i).perform()
                    sleep(2)

                    WebDriverWait(self.browser, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "fup-s-submenu-open"))
                    ).click()

                    WebDriverWait(self.browser, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "fup-s-menu-download-page-confirmation"))
                    ).click()

                    sleep(2)
                    self.browser.back()
                    sleep(3)
                    counter += 1

                    if counter == 3:  # Change to number_of_articles for full run
                        break

                if counter < 3:
                    next_button = WebDriverWait(self.browser, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "fup-archive-result-pagination-next"))
                    )
                    next_button.click()
                    sleep(2)

            except StaleElementReferenceException:
                self.browser.refresh()
                sleep(2)
