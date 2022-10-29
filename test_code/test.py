import json
from lib2to3.pgen2 import driver
from tokenize import cookie_re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import time
import pickle

class Chrome():

    URL = 'https://www.fugle.tw'
    CHROME_LOCATION = os.getcwd() + '/chromedriver'
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    object = Service(CHROME_LOCATION)
    driver = webdriver.Chrome(service=object, options=chrome_options)
    
    def __init__(self):
        self.driver.get(self.URL)
        self.driver.set_window_size(1920, 1080)
        time.sleep(20)
        

    def get_cookie(self):
        with open('fugle', 'wb') as f:
            pickle.dump(self.driver.get_cookies(), f)

    def use_cookie(self):
        with open("fugle", 'rb')as file:
            fugle_cookie = pickle.load(file)
            for cookie in fugle_cookie:
                self.driver.add_cookie(cookie)
        print('start fresh')
        self.driver.refresh()

if __name__ == "__main__":
    chrome = Chrome()
    # chrome.get_cookie()
    chrome.use_cookie()