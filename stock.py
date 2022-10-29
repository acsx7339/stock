#!/usr/bin/python 
#-*-coding:utf-8-*-
from genericpath import isdir
from re import X
import requests
import pandas as pd
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pickle


class Folder():
    def __init__(self):
        self.DeleteoldFolder()
        self.CreateFolder()

    def CreateFolder(self):
        folder_name = datetime.datetime.today().strftime('%Y%m%d')
        path = os.getcwd()
        folder_location = path + '/date/' + folder_name
        if os.path.exists(folder_location):
            pass
        else:
            os.mkdir(folder_location)
            print(f'create folder {folder_location}')

    def DeleteoldFolder(self):
        path = os.getcwd()
        old_folder_path = path + "/date/" 
        print(old_folder_path)
        if any(x.startswith('202') for x in os.listdir(old_folder_path)):
            os.system(f'rm -rf {old_folder_path}/*')
            print('remove all old folder')
        else:
            print('there is no old folder')
            pass


class GoodInfo():
    url = "https://goodinfo.tw/tw2/StockList.asp?MARKET_CAT=%E8%87%AA%E8%A8%82%E7%AF%A9%E9%81%B8&INDUSTRY_CAT=%E6%88%91%E7%9A%84%E6%A2%9D%E4%BB%B6&FL_ITEM0=&FL_VAL_S0=&FL_VAL_E0=&FL_ITEM1=&FL_VAL_S1=&FL_VAL_E1=&FL_ITEM2=&FL_VAL_S2=&FL_VAL_E2=&FL_ITEM3=&FL_VAL_S3=&FL_VAL_E3=&FL_ITEM4=&FL_VAL_S4=&FL_VAL_E4=&FL_ITEM5=&FL_VAL_S5=&FL_VAL_E5=&FL_ITEM6=&FL_VAL_S6=&FL_VAL_E6=&FL_ITEM7=&FL_VAL_S7=&FL_VAL_E7=&FL_ITEM8=&FL_VAL_S8=&FL_VAL_E8=&FL_ITEM9=&FL_VAL_S9=&FL_VAL_E9=&FL_ITEM10=&FL_VAL_S10=&FL_VAL_E10=&FL_ITEM11=&FL_VAL_S11=&FL_VAL_E11=&FL_RULE0=%E5%9D%87%E7%B7%9A%E4%BD%8D%E7%BD%AE%7C%7C%E5%9D%87%E5%83%B9%E7%B7%9A%E7%9B%B8%E4%BA%92%E7%B3%BE%E7%B5%90+%2810%E6%97%A5%2F%E6%9C%88%E7%B7%9A%29%40%40%E5%9D%87%E5%83%B9%E7%B7%9A%E7%9B%B8%E4%BA%92%E7%B3%BE%E7%B5%90%40%4010%E6%97%A5%2F%E6%9C%88%E7%B7%9A&FL_RULE1=&FL_RULE2=&FL_RULE3=&FL_RULE4=&FL_RULE5=&FL_RANK0=&FL_RANK1=&FL_RANK2=&FL_RANK3=&FL_RANK4=&FL_RANK5=&FL_FD0=%E5%88%86%E7%B4%9A%E6%8C%81%E6%9C%89%E6%AF%94%E4%BE%8B%E9%80%B1%E5%A2%9E%E6%B8%9B%E6%95%B8%E2%80%9340%E5%BC%B5%E4%BB%A5%E4%B8%8B%E2%80%93%E7%95%B6%E9%80%B1%7C%7C1%7C%7C0%7C%7C%3C%7C%7C%E5%88%86%E7%B4%9A%E6%8C%81%E6%9C%89%E6%AF%94%E4%BE%8B%E9%80%B1%E5%A2%9E%E6%B8%9B%E6%95%B8%E2%80%9340%E5%BC%B5%E4%BB%A5%E4%B8%8B%E2%80%93%E5%89%8D1%E9%80%B1%7C%7C1%7C%7C0&FL_FD1=&FL_FD2=&FL_FD3=&FL_FD4=&FL_FD5=&FL_SHEET=%E5%B9%B4%E7%8D%B2%E5%88%A9%E8%83%BD%E5%8A%9B&FL_SHEET2=%E7%8D%B2%E5%88%A9%E8%83%BD%E5%8A%9B&FL_MARKET=%E4%B8%8A%E5%B8%82%2F%E4%B8%8A%E6%AB%83&FL_QRY=%E6%9F%A5++%E8%A9%A2"
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}
    stock_list = []

    def stocklist(self):
        request_data = requests.get(self.url, headers = self.headers)
        request_data.encoding='utf-8'
        soup = BeautifulSoup(request_data.text,"lxml")
        data = soup.select_one("#txtStockListData")
        dfs = pd.read_html(data.prettify())
        dff = dfs[1]
        stock_data = list(dff['代號'])
        for item in stock_data:
            if len(str(item)) == 4:
                self.stock_list.append(item)
        print("stock list: ", self.stock_list)
        print('stock counts: ',len(self.stock_list))
        return self.stock_list
   

class Fugle():
    

    def __init__(self):
        self.URL = 'https://www.fugle.tw'
        self.FAIL_ITEM=[]
        CHROME_LOCATION = os.getcwd() + '/chromedriver'
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        object = Service(CHROME_LOCATION)
        self.driver = webdriver.Chrome(service=object, options=chrome_options)
        self.driver.get(self.URL)
        self.driver.maximize_window()
        self.usecookie()
        self.close_side()

    def usecookie(self):
        with open("fugle", 'rb')as file:
            fugle_cookie = pickle.load(file)
            for cookie in fugle_cookie:
  
                self.driver.add_cookie(cookie)
        print('get cookies, and start refresh browser')
        self.driver.refresh()

    def close_side(self):
        try:
            side_element = self.driver.find_element(By.XPATH, '//*[@id="ember14"]/header/div[3]/div[2]')
            side_element.click()
        except:
            print('close side bar failed')
            pass

    def start_filter(self, item):
        if (self.monthly_price(item) and self.monthle_tangled(item)):
            self.daily_status()
            self.screen_shot(item)

    def monthly_price(self, item):
        try:
            WebDriverWait(self.driver,30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ember17"]')))
            input_element = self.driver.find_element(By.XPATH, '//*[@id="ember17"]')
            input_element.click()
            input_element.send_keys(item)
            input_element.send_keys(Keys.RETURN)
            WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "月")]')))
            monthly_location = self.driver.find_element(By.XPATH, '//button[contains(text(), "月")]')
            monthly_location.click()
            element = self.driver.find_element(By.XPATH, '//span[@class="custom-control-description blue"]')
            price_level = int(float((element.text).split('%')[0].split(':')[1]))
            if(price_level < 65):
                print(f'{item} price level is: {price_level}')
                return True
            else:
                print(f'{item} price level is: {price_level}, so failed')         
        except Exception as e:
            print(f'monthly price failed stock: ***{item}***, root cause is {e}')
            self.FAIL_ITEM.append(item)
            self.clean()

    def monthle_tangled(self, item):
        try:
            thread_element = self.driver.find_element(By.XPATH, '//div[@class="legend-ma"]')
            short = float(thread_element.text.split('短多線:', 1)[1].split(' ')[0])
            middle = float(thread_element.text.split('中多線:', 1)[1].split(' ')[0])
            if middle * 0.93 <= short <= middle * 1.07:
                print(f'{item} is tangled')
                return True
            else:
                print(f'{item} is not tangled, so failed')
        except Exception as e:
            print(f'monthly tangled failed stock: ***{item}***, root cause is {e}')
            self.FAIL_ITEM.append(item)
            self.clean()

    def daily_status(self):
        WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "日")]')))
        daily_location = self.driver.find_element(By.XPATH, '//button[contains(text(), "日")]')
        daily_location.click()

    def screen_shot(self, item):
        folder_name = datetime.datetime.today().strftime('%Y%m%d')
        path = os.getcwd()
        folder_location = path + '/date/' + folder_name
        self.driver.execute_script("document.body.style.zoom='65%'")
        self.driver.get_screenshot_as_file(f'{folder_location}/{item}.png')
        print(f'the stock ***{item}*** test pass, and take screen shot')
        self.driver.execute_script("document.body.style.zoom='100%'")
        self.clean()
    
    def clean(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ember17"]')))
        self.driver.find_element(By.XPATH, '//*[@id="ember17"]').clear()

    def close(self):
        self.driver.close()


if __name__ == "__main__":
    folder = Folder()
    goodinfo = GoodInfo()
    goodinfo_list = goodinfo.stocklist()
    fugle = Fugle()
    for item in goodinfo_list:
        print(f'current test stock: {item}')
        fugle.start_filter(item)
    fugle.close()
    if (len(fugle.FAIL_ITEM))==0:
        print('there is no failed stock')
    else:
        print(f'here is the failed stock {fugle.FAIL_ITEM}')
        