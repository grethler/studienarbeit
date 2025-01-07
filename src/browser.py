#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Authors: Florian Grethler <grethlef@dhbw-loerrach.de>
#          Ronald Wagner <wagnerr@dhbw-loerrach.de>

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService


class Browser:
    def __init__(self, logger, settings):
        opts = Options()
        #opts.add_argument("--headless")
        opts.add_argument("--disable-gpu")
        self.browser = webdriver.Chrome(
            service=ChromeService(),
            options=opts)
        self.logger = logger
        self.settings = settings

    def login_nzz(self):

        #open URL
        self.browser.get(self.settings["urls"]["NZZ"])

        #focus on login form + login
        self.browser.find_element(By.CLASS_NAME, "fup-login").click()
        sleep(1)
        iframe = self.browser.find_element(By.XPATH, "/html/body/div[3]/div/iframe")
        self.browser.switch_to.frame(iframe)
        path = '//*[@id="autofill-form"]/screen-login/p['
        self.browser.find_element(By.XPATH, path+'3]/input').send_keys(self.settings["email"])
        self.browser.find_element(By.XPATH, path+'4]/input').send_keys(self.settings["password"])
        self.browser.find_element(By.XPATH, path+'6]/button').click()
        self.browser.switch_to.default_content()
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
        while True:
            elements = self.browser.find_elements(By.CLASS_NAME, "fup-archive-result-item-article")
            for i in elements:
                actions = ActionChains(self.browser)
                actions.move_to_element(i).perform()
                actions.click(i).perform()
                sleep(2)
                self.browser.find_element(By.CLASS_NAME, "fup-s-submenu-open").click()
                self.browser.find_element(By.CLASS_NAME, "fup-s-menu-download-page-confirmation").click()
                sleep(2)
                self.browser.back()
                counter += 1
            if counter == 3: #== number_of_articles:
                break
        sleep(1000)

    def switchTabContext(self):
        pass
