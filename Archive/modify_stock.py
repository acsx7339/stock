#!/usr/bin/python 
#-*-coding:utf-8-*-
import requests
import pandas as pd
import datetime
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import json
from selenium.common.exceptions import WebDriverException


class stock_list():

    def stock_list(self):
        headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}
        url = "https://goodinfo.tw/tw/StockList.asp?MARKET_CAT=%E8%87%AA%E8%A8%82%E7%AF%A9%E9%81%B8&INDUSTRY_CAT=%E6%88%91%E7%9A%84%E6%A2%9D%E4%BB%B6&FL_ITEM0=%E5%88%86%E7%B4%9A%E6%8C%81%E6%9C%89%E6%AF%94%E4%BE%8B%E9%80%B1%E5%A2%9E%E6%B8%9B%E6%95%B8%E2%80%9350%E5%BC%B5%E4%BB%A5%E4%B8%8B&FL_VAL_S0=&FL_VAL_E0=0&FL_ITEM1=%E5%88%86%E7%B4%9A%E6%8C%81%E6%9C%89%E6%AF%94%E4%BE%8B%E9%80%B1%E5%A2%9E%E6%B8%9B%E6%95%B8%E2%80%93%E8%B6%85%E9%81%8E400%E5%BC%B5&FL_VAL_S1=0&FL_VAL_E1=&FL_ITEM2=&FL_VAL_S2=&FL_VAL_E2=&FL_ITEM3=&FL_VAL_S3=&FL_VAL_E3=&FL_ITEM4=&FL_VAL_S4=&FL_VAL_E4=&FL_ITEM5=&FL_VAL_S5=&FL_VAL_E5=&FL_ITEM6=&FL_VAL_S6=&FL_VAL_E6=&FL_ITEM7=&FL_VAL_S7=&FL_VAL_E7=&FL_ITEM8=&FL_VAL_S8=&FL_VAL_E8=&FL_ITEM9=&FL_VAL_S9=&FL_VAL_E9=&FL_ITEM10=&FL_VAL_S10=&FL_VAL_E10=&FL_ITEM11=&FL_VAL_S11=&FL_VAL_E11=&FL_RULE0=&FL_RULE1=&FL_RULE2=&FL_RULE3=&FL_RULE4=&FL_RULE5=&FL_RANK0=&FL_RANK1=&FL_RANK2=&FL_RANK3=&FL_RANK4=&FL_RANK5=&FL_FD0=&FL_FD1=&FL_FD2=&FL_FD3=&FL_FD4=&FL_FD5=&FL_SHEET=%E5%B9%B4%E7%8D%B2%E5%88%A9%E8%83%BD%E5%8A%9B&FL_SHEET2=%E7%8D%B2%E5%88%A9%E8%83%BD%E5%8A%9B&FL_MARKET=%E4%B8%8A%E5%B8%82%2F%E4%B8%8A%E6%AB%83&FL_QRY=%E6%9F%A5++%E8%A9%A2"
        res = requests.get(url, headers = headers)
        res.encoding='utf-8'
        soup = BeautifulSoup(res.text,"lxml")
        data = soup.select_one("#txtStockListData")
        dfs = pd.read_html(data.prettify())
        dff = dfs[1]
        stock_data = list(dff['代號'])
        return stock_data

    def filter_stock(self, item):
        stock_list = []
        for stock in item:
            if len(stock) == 4:
                stock_list.append(stock)
        return stock_list

class fugle():

    folder_name = datetime.datetime.today().strftime('%Y%m%d')

    def folder(self):
        dir = f"./{self.folder_name}"
        if os.path.exists(dir):
            pass
        else:
            os.makedirs(dir)

    def weekly_filter(self, stock, driver):
        print('Test stock: ', stock)
        WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.ID, "ember20")))
        input_element = driver.find_element(By.ID, "ember20")
        input_element.send_keys(stock)
        input_element.send_keys(Keys.RETURN)
        driver.execute_script("document.body.style.zoom='50%'")
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "周")]')))
        link = driver.find_element(By.XPATH, '//button[contains(text(), "周")]')
        driver.execute_script("arguments[0].click();", link)
        thread_element = driver.find_element(By.XPATH, '//div[@class="legend-ma"]')
        short = float(thread_element.text.split('短多線:', 1)[1].split(' ')[0])
        middle = float(thread_element.text.split('中多線:', 1)[1].split(' ')[0])
        if middle * 0.93 <= short <= middle * 1.07:
            return True

    def monthly_filter(self, stock, driver):
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "月")]')))
        link = driver.find_element(By.XPATH, '//button[contains(text(), "月")]')
        driver.execute_script("arguments[0].click();", link)
        element = driver.find_element(By.XPATH, '//span[@class="custom-control-description blue"]')
        pl = float((element.text).split('%')[0].split(':')[1])
        thread_element = driver.find_element(By.XPATH, '//div[@class="legend-ma"]')
        short = float(thread_element.text.split('短多線:', 1)[1].split(' ')[0])
        middle = float(thread_element.text.split('中多線:', 1)[1].split(' ')[0])
        if pl < 65 and middle * 0.93 <= short <= middle * 1.07:
            print(f'{stock} pass the filter')
            self.screenshot(stock, driver)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "ember20")))
        driver.find_element(By.ID, "ember20").clear()

    def screenshot(self, item, driver):
        driver.save_screenshot('./{}/{}.png'.format(self.folder_name, item))

class Chrome():

    def __init__(self):
        self.option()

    def option(self):
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        url = 'https://www.fugle.tw' 
        self.driver = webdriver.Chrome('./chromedriver', options=chrome_options)
        self.driver.set_window_size(1366, 728)
        self.driver.get(url)
        with open ('fugle.json', 'r') as f:
            data = json.loads(f.read())
            for item in data:
                self.driver.add_cookie(item)
            self.driver.refresh()
        self.driver.maximize_window()

if __name__=="__main__":
    # goodinof_result = stock_list().stock_list()
    # total_stock = stock_list().filter_stock(goodinof_result)
    # print(total_stock)
    # print('*** Total stock item number ***',len(total_stock))
    fugle().folder()
    total_stock = ['8050', '8059', '8071', '8072', '8077', '8081', '8083', '8088', '8099', '8109', '8121', '8147', '8171', '8182', '8183', '8201', '8222', '8240', '8261', '8277', '8279', '8284', '8291', '8299', '8349', '8367', '8374', '8401', '8409', '8415', '8416', '8420', '8423', '8426', '8446', '8455', '8467', '8472', '8476', '8477', '8478', '8480', '8499', '8905', '8917', '8921', '8923', '8928', '8930', '8933', '8935', '8937', '8938', '8940', '9103', '9188', '9908', '9911', '9918', '9919', '9925', '9927', '9928', '9929', '9931', '9933', '9934', '9935', '9940', '9942', '9944', '9949', '9950', '9955', '9962']
    fugle_website = Chrome().driver
    fail_stock = []
    for item in total_stock:
        try:
            weekly_result = fugle().weekly_filter(item, fugle_website)
        except:
            fail_stock.append(item)
        if weekly_result:
            try:
                fugle().monthly_filter(item, fugle_website)
            except:
                fail_stock.append(item)