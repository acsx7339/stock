#coding:utf-8
from numpy.lib.histograms import _search_sorted_inclusive
import pandas as pd
from bs4 import BeautifulSoup
import requests
from io import StringIO
import time
import numpy as np
import random
from fake_useragent import UserAgent
import re
from scraper_api import ScraperAPIClient
import datetime
from datetime import timedelta
import pandas_datareader as pdr
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.keys import Keys 
import os
import twstock
from dateutil.relativedelta import relativedelta
import logging
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
todate = date.today()
logging.basicConfig(level=logging.DEBUG, filename=f'{todate}.log', filemode='w', format=FORMAT)


def sotck_list():  
    res = requests.get("https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&")
    df = pd.read_html(res.text)[0]
    df = df.drop([0,1,3,4,5,6,7,8,9], axis=1)
    df.columns = df.iloc[0]
    df = df.iloc[1:]
    res2 = requests.get("https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=4&industry_code=&Page=1&chklike=Y")
    df2 = pd.read_html(res2.text)[0]
    df2 = df2.drop([0,1,3,4,5,6,7,8,9], axis=1)
    df2.columns = df2.iloc[0]
    df2 = df2.iloc[1:]
    whole_stock_list = sorted(df['有價證券代號'].to_list() + df2['有價證券代號'].to_list())
    print(whole_stock_list)
    print('---------------')
    whole_stock_list_number = len(sorted(df['有價證券代號'].to_list() + df2['有價證券代號'].to_list()))
    print('total counts of stock: ', whole_stock_list_number)
    print('---------------')
    return(sorted(df['有價證券代號'].to_list() + df2['有價證券代號'].to_list()))

def get_100d_data(stock):
    value_list = []
    one_hundred_day_ago = datetime.timedelta(days = 143)
    start = datetime.datetime.now() - one_hundred_day_ago
    end   = datetime.datetime.now()
    try:        
        DataFrame = pdr.DataReader(stock+'.TW', 'yahoo', start, end)
        close_array = DataFrame['Close']
        max_value = round(max(close_array), 2)
        min_value = round(min(close_array), 2)
        current_value = round(close_array[-1], 2)
        value_list =[stock, current_value, max_value, min_value]
        print(value_list)
        return(value_list)
    except:
        try:
            DataFrame = pdr.DataReader(stock+'.TWO', 'yahoo', start, end)
            close_array = DataFrame['Close']
            max_value = round(max(close_array), 2)
            min_value = round(min(close_array), 2)
            current_value = round(close_array[-1], 2)
            value_list =[stock, current_value, max_value, min_value]
            print(value_list)
            return(value_list)
        except:
            pass


def price_level(stockinfo):
    try:
        watch_stock = ''
        upper_value = float(stockinfo[1]) - float(stockinfo[3])
        lower_value = float(stockinfo[2]) - float(stockinfo[3])
        ratio =  upper_value/lower_value
        print(f'the stock {stockinfo[0]} ratio is: {ratio}' )
        if ratio < 0.7 and ratio > 0.1:
            watch_stock = stockinfo[0]
            print('PASS')
        return (watch_stock)
    except Exception as e:
        #the min value = current, div by zero
        print("FAIL")
        pass 
def stockholder(stock):
    try:
        end_date = datetime.datetime.now()
        start_day = (datetime.datetime.today() - datetime.timedelta(days=time.localtime().tm_wday + 30)).strftime("%Y-%m-%d")
        url = "https://api.finmindtrade.com/api/v3/data"
        parameter = {
                "dataset": "TaiwanStockHoldingSharesPer",
                "stock_id": stock,
                "date": start_day,
                "end_date": end_date,
                "user_id": 'acsx7339',
                "password": 'sjwd5407'
            }
        data = requests.get(url, params=parameter)
        data = data.json()
        data = pd.DataFrame(data['data'])
        day = data['date'].unique()
        mask1 = data['HoldingSharesLevel'].isin(['1-999','1,000-5,000','5,001-10,000','10,001-15,000','15,001-20,000','20,001-30,000','30,001-40,000','40,001-50,000'])
        mask2 = (data['date'] == day[-2])
        mask3 = (data['date'] == day[-1])
        df_old = data[(mask1 & mask2)]
        df_new = data[(mask1 & mask3)]
        value_old = df_old['percent'].sum()
        value_new = df_new['percent'].sum()
        if value_old > value_new:
            stockholdervalue = value_old - value_new
            print('stock decrease value: ',stockholdervalue)
            return stock
    except:
        print('sleep one hour')
        time.sleep(3600)

def showdate():
    end_date = datetime.datetime.now()
    start_day = (datetime.datetime.today() - datetime.timedelta(days=time.localtime().tm_wday + 30)).strftime("%Y-%m-%d")
    url = "https://api.finmindtrade.com/api/v3/data"
    parameter = {
            "dataset": "TaiwanStockHoldingSharesPer",
            "stock_id": '2330',
            "date": start_day,
            "end_date": end_date,
            "user_id": 'acsx7339',
            "password": 'sjwd5407'
        }
    data = requests.get(url, params=parameter)
    data = data.json()
    data = pd.DataFrame(data['data'])
    day = data['date'].unique()
    print('--------------------------------')
    print('start day: ', day[-2],'end day: ',day[-1])
    print('--------------------------------')


def open_fugle(stockList):
    folder = datetime.datetime.today().strftime('%Y%m%d')
    fail_stock=[]
    url = 'https://www.fugle.tw' 
    driver = webdriver.Chrome('/Users/fachu/Desktop/python/StockPicking/chromedriver')
    driver.get(url)
    driver.maximize_window()
    ActionChains(driver).move_by_offset(200, 100).click().perform()
    time.sleep(1)
    driver.find_element_by_class_name("ember-view.btn.btn-primary.mr-2.login-btn").click()
    time.sleep(1)
    driver.find_element_by_css_selector(("[class='ember-text-field ember-view form-control form-control-lg mb-2']")).send_keys("0938922392")
    driver.find_element_by_class_name("btn-submit").click()
    time.sleep(1)
    driver.find_element_by_class_name("ember-text-field.ember-view.form-control.form-control-lg.mb-2.input-auth").send_keys("sjwd5407")
    driver.find_element_by_class_name("btn-submit").click()
    os.mkdir(f'/Users/fachu/Desktop/python/StockPicking/{folder}/')
    for item in stockList:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "ember19")))
        input_element = driver.find_element_by_id("ember19")
        input_element.send_keys(item)
        input_element.send_keys(Keys.RETURN)
        driver.execute_script("document.body.style.zoom='50%'")
        # driver.execute_script("window.scrollTo(0, 500)")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "月")]')))
        link = driver.find_element_by_xpath('//button[contains(text(), "月")]')
        driver.execute_script("arguments[0].click();", link)
        driver.get_screenshot_as_file(f'/Users/fachu/Desktop/python/StockPicking/{folder}/{item}.png')
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "ember19")))
        driver.find_element_by_id("ember19").clear()

    # print('stock holder failed stock: ',fail_stock)

if __name__ == "__main__":
    showdate()
    pl_list = []
    sh_list = []
    for item in sotck_list():
        print('price level filter stock: ', item)
        one_hundred_data = get_100d_data(item)
        pl_list.append(price_level(one_hundred_data))
    pl_list = list(filter(None, pl_list))
    logging.info(pl_list)
    print('price level list: ',pl_list)
    print('---------------')
    print('price level list counts: ', len(pl_list))
    print('---------------')
    for item in pl_list:
        print('stock holder filter stock: ', item)
        sh_list.append(stockholder(item))
    sh_list = list(filter(None, sh_list))
    logging.info(sh_list)
    print('stock holder list: ',sh_list)
    print('---------------')
    print('stock holder count: ', len(sh_list))
    print('---------------')
    open_fugle(sh_list)