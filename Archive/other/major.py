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
import datetime as datetime
import pandas_datareader as pdr
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.keys import Keys 
import os


one_hundred_day_ago = datetime.timedelta(days = 143)
start_day = datetime.datetime.now() - one_hundred_day_ago
end_day = datetime.datetime.now()
stockhold_problem = []
pricelevel_problem_stock = []
one_week_ago = (datetime.datetime.today() - datetime.timedelta(days=time.localtime().tm_wday + 3)).strftime("%Y-%m-%d")
two_week_ago = (datetime.datetime.today() - datetime.timedelta(days=time.localtime().tm_wday + 10)).strftime("%Y-%m-%d")
print('two_week_ago : ',two_week_ago)
print('one_week_ago : ',one_week_ago)

def sotck_list():  
    res = requests.get("https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&")
    df = pd.read_html(res.text)[0]
    df = df.drop([0,1,3,4,5,6,7,8,9], axis=1)
    df.columns = df.iloc[0]
    df = df.iloc[1:]
    # print(df['有價證券代號'].to_list())
    return(df['有價證券代號'].to_list())


def high_and_low(code):
    value_list = []
    start = start_day
    end   = end_day
    try:        
        DataFrame = pdr.DataReader(code+'.TW', 'yahoo', start, end)
        close_array = DataFrame['Close']
        max_value = round(max(close_array), 2)
        # print(max_value)
        min_value = round(min(close_array), 2)
        # print(min_value)
        current_value = round(close_array[-1], 2)
        # print('target stock: ', code,'max price: ', max_value, 'min price:', min_value, 'current price:', current_value)
        if current_value > 10:
            value_list =[code, current_value, max_value, min_value]
            print(value_list)
            return(value_list)
        
    except:
        DataFrame = pdr.DataReader(code+'.TWO', 'yahoo', start, end)
        close_array = DataFrame['Close']
        max_value = round(max(close_array), 2)
        # print(max_value)
        min_value = round(min(close_array), 2)
        # print(min_value)
        current_value = round(close_array[-1], 2)
        # print('target stock: ', code,'max price: ', max_value, 'min price:', min_value, 'current price:', current_value)
        if current_value > 10:
            value_list =[code, current_value, max_value, min_value]
            print(value_list)
            return(value_list)
    

def price_level_yahoo(ratio_stock):
    print('test ratio stock',ratio_stock)
    try:
        watch_stock = ''
        upper_value = float(ratio_stock[1]) - float(ratio_stock[3])
        lower_value = float(ratio_stock[2]) - float(ratio_stock[3])
        ratio =  upper_value/lower_value
        print('ratio: ' ,ratio)
        if ratio < 0.7 and ratio > 0.1:
            watch_stock = ratio_stock[0]
            # print(watch_stock)
            print('ration < 65:',watch_stock)
        return (watch_stock)
    # print('code: ', watch_stock, 'ratio: ', ratio)
    except :
        pricelevel_problem_stock.append(ratio_stock[0])
    


def compare_stockhold(stock):
    two_week_ago_value = get_stockhold_ratio(stock, two_week_ago)
    one_week_ago_value = get_stockhold_ratio(stock, one_week_ago)
    if two_week_ago_value - one_week_ago_value > 0:
        print('result: ',stock)
        return stock
        

def get_stockhold_ratio(stock, day):
    try:
        url = "https://api.finmindtrade.com/api/v3/data"
        parameter = {
                "dataset": "TaiwanStockHoldingSharesPer",
                "stock_id": stock,
                "date": day,
                "user_id": 'sjwd5407',
                "password": 'acsx7339'
            }
        data = requests.get(url, params=parameter)
        data = data.json()
        data = pd.DataFrame(data['data'])
        value = float(data.at[0, 'percent'])+float(data.at[1, 'percent'])+float(data.at[2, 'percent'])+float(data.at[3, 'percent'])+float(data.at[4, 'percent'])+float(data.at[5, 'percent'])+float(data.at[6, 'percent'])+float(data.at[7, 'percent'])
        return value
    except:
        stockhold_problem.append(stock)
        return 0

def open_fugle(stockList):
    folder = datetime.datetime.today().strftime('%Y%m%d')
    fail_stock=[]
    url = 'https://www.fugle.tw' 
    driver = webdriver.Chrome('/Users/fachu/Desktop/stock_photo/chromedriver')
    driver.get(url)
    driver.maximize_window()
    ActionChains(driver).move_by_offset(200, 100).click().perform()
    driver.find_element_by_id("ember24").click()
    driver.find_element_by_id("ember89").send_keys("0938922392")
    driver.find_element_by_class_name("btn-submit").click()
    time.sleep(1)
    driver.find_element_by_id("ember92").send_keys("sjwd5407")
    driver.find_element_by_class_name("btn-submit").click()
    time.sleep(5)
    os.mkdir(f'/Users/fachu/Desktop/python_test/StockPicking/{folder}/')
    for item in stockList:
        try:
            driver.find_element_by_id("ember19").send_keys(item)
            driver.find_element_by_id("ember19").send_keys(Keys.RETURN)
            driver.execute_script("document.body.style.zoom='0.4'")
            time.sleep(2)
            scroll_location = driver.find_element_by_class_name('note-textarea')
            scroll_location.location_once_scrolled_into_view
            time.sleep(5)
            driver.get_screenshot_as_file(f'/Users/fachu/Desktop/python_test/StockPicking/{folder}/{item}.png')
            driver.find_element_by_id("ember19").clear()
        except:
            fail_stock.append(item)
            driver.find_element_by_id("ember19").clear()
    print(fail_stock)
            
        

if __name__ == "__main__":
    stocklist = []
    all_list = sotck_list()
    print(all_list)
    for item in all_list:
        each_stock = high_and_low(item)
        if each_stock is not None:
            stocklist.append(price_level_yahoo(each_stock))
    sotck_list_without_empty = [x for x in stocklist if x != '' ]
    print('PL stock list:',sotck_list_without_empty)
    print(len(sotck_list_without_empty))
    result = []
    for item in sotck_list_without_empty:
        result.append(compare_stockhold(item))
    result = [x for x in result if x != None ]
    print('retail list: ',result)
    print('stockhold_problem: ',stockhold_problem)
    print('pricelevel_problem_stock: ', pricelevel_problem_stock)
    open_fugle(result)
