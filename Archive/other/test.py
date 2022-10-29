import pandas as pd
import pandas_datareader as pdr
import requests
from bs4 import BeautifulSoup
from scraper_api import ScraperAPIClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.keys import Keys 
from dateutil.relativedelta import relativedelta
from datetime import datetime
import calendar
import datetime
from datetime import timedelta
from datetime import date

# def open_fugle():
#     url = 'https://www.fugle.tw' 
#     driver = webdriver.Chrome('/Users/fachu/Desktop/stock_photo/chromedriver')
#     driver.get(url)
#     driver.maximize_window()
#     ActionChains(driver).move_by_offset(200, 100).click().perform()
#     driver.find_element_by_id("ember24").click()
#     driver.find_element_by_id("ember89").send_keys("0938922392")
#     driver.find_element_by_class_name("btn-submit").click()
#     time.sleep(1)
#     driver.find_element_by_id("ember92").send_keys("sjwd5407")
#     driver.find_element_by_class_name("btn-submit").click()
#     time.sleep(5)
#     driver.find_element_by_id("ember19").send_keys("2330")
#     driver.find_element_by_id("ember19").send_keys(Keys.RETURN)
#     driver.execute_script("document.body.style.zoom='0.4'")
#     time.sleep(2)
#     scroll_location = driver.find_element_by_class_name('note-textarea')
#     scroll_location.location_once_scrolled_into_view
#     time.sleep(5)
#     driver.get_screenshot_as_file('/Users/fachu/Desktop/python_test/StockPicking/test.png')
#     driver.find_element_by_id("ember19").clear()
#     time.sleep(5)

# def compare_stockhold(stock):
#     one_week_ago = (datetime.datetime.today() - datetime.timedelta(days=time.localtime().tm_wday + 4)).strftime("%Y-%m-%d")
#     two_week_ago = (datetime.datetime.today() - datetime.timedelta(days=time.localtime().tm_wday + 10)).strftime("%Y-%m-%d")
#     print('two_week_ago : ',two_week_ago)
#     print('one_week_ago : ',one_week_ago)
#     two_week_ago_value = get_stockhold_ratio(stock, two_week_ago)
#     one_week_ago_value = get_stockhold_ratio(stock, one_week_ago)
#     print('two week ago: ',two_week_ago_value)
#     print('one week ago: ', one_week_ago_value)
#     if two_week_ago_value - one_week_ago_value > 0:
#         print('true')
#     else:
#         print('false')
        

# def get_stockhold_ratio(stock, day):
#     try:
#         url = "https://api.finmindtrade.com/api/v3/data"
#         parameter = {
#                 "dataset": "TaiwanStockHoldingSharesPer",
#                 "stock_id": stock,
#                 "date": day,
#                 "user_id": 'sjwd5407',
#                 "password": 'acsx7339'
#             }
#         data = requests.get(url, params=parameter)
#         data = data.json()
#         data = pd.DataFrame(data['data'])
#         print(data)
#         value = float(data.at[0, 'percent'])+float(data.at[1, 'percent'])+float(data.at[2, 'percent'])+float(data.at[3, 'percent'])+float(data.at[4, 'percent'])+float(data.at[5, 'percent'])+float(data.at[6, 'percent'])+float(data.at[7, 'percent'])
#         return value
#     except:
#         return 0
def get(stock='2330'):
    end_date = datetime.datetime.now()
    start_day = (datetime.datetime.today() - datetime.timedelta(days=time.localtime().tm_wday + 4)).strftime("%Y-%m-%d")
    url = "https://api.finmindtrade.com/api/v3/data"
    parameter = {
            "dataset": "TaiwanStockHoldingSharesPer",
            "stock_id": stock,
            "date": start_day,
            "end_date": end_date,
            "user_id": 'sjwd5407',
            "password": 'acsx7339'
        }
    data = requests.get(url, params=parameter)
    data = data.json()
    data = pd.DataFrame(data['data'])
    date = data['date'].unique()
    print(date)
    print(date[1])
    mask1 = data['HoldingSharesLevel'].isin(['1-999','1,000-5,000','5,001-10,000','10,001-15,000','15,001-20,000','20,001-30,000','30,001-40,000','40,001-50,000'])
    mask2 = (data['date'] == date[0])
    df = data[(mask1 & mask2)]
    print(df)
    # value = float(df.at[0, 'percent'])+float(df.at[1, 'percent'])+float(df.at[2, 'percent'])+float(df.at[3, 'percent'])+float(df.at[4, 'percent'])+float(df.at[5, 'percent'])+float(df.at[6, 'percent'])+float(df.at[7, 'percent'])
    value = df['percent'].sum()
    print(value)

def daay():
    print(date.today())

if __name__ == "__main__":
    # get()
    daay()