import requests
import pandas as pd
import datetime
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import pandas_datareader as pdr
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import shutil
import json
import pickle

def get_cookie():
    url = 'https://www.fugle.tw' 
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)
    time.sleep(40)
    cookie = driver.get_cookies()
    with open ('fugle.json', 'w') as f:
        f.write(json.dumps(cookie))




# def open_fugle(stockList):

#                 chrome_options = Options()
#                 # chrome_options.add_argument('--headless')
#                 chrome_options.add_argument('--no-sandbox')
#                 chrome_options.add_argument('--disable-dev-shm-usage')
#                 folder = datetime.datetime.today().strftime('%Y%m%d')
#                 url = 'https://www.fugle.tw' 
#                 driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
#                 driver.get(url)
#                 driver.maximize_window()
#                 ActionChains(driver).move_by_offset(200, 100).click().perform()
#                 time.sleep(3)
#                 driver.find_element_by_class_name("ember-view.btn.btn-primary.mr-2.login-btn").click()
#                 time.sleep(20)
#                 driver.find_element_by_css_selector(("[class='ember-text-field ember-view form-control form-control-lg mb-2']")).send_keys("0938922392")
#                 driver.find_element_by_class_name("btn-submit").click()
#                 time.sleep(1)
#                 driver.find_element_by_class_name("ember-text-field.ember-view.form-control.form-control-lg.mb-2.input-auth").send_keys("sjwd5407")
#                 driver.find_element_by_class_name("btn-submit").click()
#                 dir = f'./test{folder}'
#                 if os.path.exists(dir):
#                     pass
#                 else:
#                     os.makedirs(dir)
#                 for item in stockList:
#                     WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.ID, "ember19")))
#                     input_element = driver.find_element_by_id("ember19")
#                     input_element.send_keys(item)
#                     input_element.send_keys(Keys.RETURN)
#                     driver.execute_script("document.body.style.zoom='50%'")
#                     WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "周")]')))
#                     link = driver.find_element_by_xpath('//button[contains(text(), "周")]')
#                     driver.execute_script("arguments[0].click();", link)
                    
#                     thread_element = driver.find_element_by_xpath('//div[@class="legend-ma"]')
#                     print(thread_element.text)
#                     short = float(thread_element.text.split(' ')[0].split(':')[1])
#                     print(short)
#                     middle = float(thread_element.text.split(' ')[2].split(':')[1])
#                     print(middle)
#                     time.sleep(2)
#                     if middle * 0.93 <= short <= middle * 1.07:
#                         WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "月")]')))
#                         link = driver.find_element_by_xpath('//button[contains(text(), "月")]')
#                         driver.execute_script("arguments[0].click();", link)
#                         element = driver.find_element_by_xpath('//span[@class="custom-control-description blue"]')
#                         pl = float(element.text.split('%')[0].split(':')[1])
#                         print(pl)
#                         thread_element = driver.find_element_by_xpath('//div[@class="legend-ma"]')
#                         print(thread_element.text)
#                         short = float(thread_element.text.split(' ')[0].split(':')[1])
#                         print(short)
#                         middle = float(thread_element.text.split(' ')[2].split(':')[1])
#                         print(middle)
#                         time.sleep(2)
#                         if pl < 65 and middle * 0.93 <= short <= middle * 1.07:
#                             driver.get_screenshot_as_file(f'{dir}/{item}.png')
#                     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "ember19")))
#                     driver.find_element_by_id("ember19").clear()                    
           


if __name__ == "__main__":
    # st_list = ['3466', '2330']
    # open_fugle(st_list)
    # a = '短多線:10.0 中多線:10.7 arrow_drop_down 長多線:8.0 arrow_drop_up'
    # b = '短多線:138.1 arrow_drop_down 中多線:144.8 arrow_drop_down 長多線:144.6 arrow_drop_down'
    # middle = (a.split('短多線:', 1)[1].split(' ')[0])
    # print(middle)
    get_cookie()