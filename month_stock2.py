import requests
import pandas as pd
import datetime
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas_datareader as pdr
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import shutil
from selenium.common.exceptions import WebDriverException


def goodinfo():
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}
    url = "https://goodinfo.tw/StockInfo/StockList.asp?MARKET_CAT=%E8%87%AA%E8%A8%82%E7%AF%A9%E9%81%B8&INDUSTRY_CAT=%E6%88%91%E7%9A%84%E6%A2%9D%E4%BB%B6&FL_ITEM0=%E5%88%86%E7%B4%9A%E6%8C%81%E6%9C%89%E6%AF%94%E4%BE%8B%E9%80%B1%E5%A2%9E%E6%B8%9B%E6%95%B8%E2%80%9350%E5%BC%B5%E4%BB%A5%E4%B8%8B&FL_VAL_S0=&FL_VAL_E0=0&FL_ITEM1=%E5%88%86%E7%B4%9A%E6%8C%81%E6%9C%89%E6%AF%94%E4%BE%8B%E9%80%B1%E5%A2%9E%E6%B8%9B%E6%95%B8%E2%80%93%E8%B6%85%E9%81%8E400%E5%BC%B5&FL_VAL_S1=0&FL_VAL_E1=&FL_ITEM2=&FL_VAL_S2=&FL_VAL_E2=&FL_ITEM3=&FL_VAL_S3=&FL_VAL_E3=&FL_ITEM4=&FL_VAL_S4=&FL_VAL_E4=&FL_ITEM5=&FL_VAL_S5=&FL_VAL_E5=&FL_ITEM6=&FL_VAL_S6=&FL_VAL_E6=&FL_ITEM7=&FL_VAL_S7=&FL_VAL_E7=&FL_ITEM8=&FL_VAL_S8=&FL_VAL_E8=&FL_ITEM9=&FL_VAL_S9=&FL_VAL_E9=&FL_ITEM10=&FL_VAL_S10=&FL_VAL_E10=&FL_ITEM11=&FL_VAL_S11=&FL_VAL_E11=&FL_RULE0=&FL_RULE1=&FL_RULE2=&FL_RULE3=&FL_RULE4=&FL_RULE5=&FL_RANK0=&FL_RANK1=&FL_RANK2=&FL_RANK3=&FL_RANK4=&FL_RANK5=&FL_FD0=&FL_FD1=&FL_FD2=&FL_FD3=&FL_FD4=&FL_FD5=&FL_SHEET=%E5%B9%B4%E7%8D%B2%E5%88%A9%E8%83%BD%E5%8A%9B&FL_SHEET2=%E7%8D%B2%E5%88%A9%E8%83%BD%E5%8A%9B&FL_MARKET=%E4%B8%8A%E5%B8%82%2F%E4%B8%8A%E6%AB%83&FL_QRY=%E6%9F%A5++%E8%A9%A2"
    res = requests.get(url, headers = headers)
    res.encoding='utf-8'
    soup = BeautifulSoup(res.text,"lxml")
    data = soup.select_one("#txtStockListData")
    dfs = pd.read_html(data.prettify())
    dff = dfs[1]
    stock_data = list(dff['代號'])
    stock_list = []
    for item in stock_data:
        if len(item) == 4:
            stock_list.append(item)
    print(stock_list)
    print('-------',len(stock_list))
    return stock_list

def open_fugle(stockList):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    folder = datetime.datetime.today().strftime('%Y%m%d')
    url = 'https://www.fugle.tw' 
    driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
    driver.get(url)
    driver.maximize_window()
    ActionChains(driver).move_by_offset(200, 100).click().perform()
    time.sleep(3)
    driver.find_element_by_class_name("ember-view.btn.btn-primary.mr-2.login-btn").click()
    time.sleep(3)
    driver.find_element_by_css_selector(("[class='ember-text-field ember-view form-control form-control-lg mb-2']")).send_keys("0938922392")
    driver.find_element_by_class_name("btn-submit").click()
    time.sleep(1)
    driver.find_element_by_class_name("ember-text-field.ember-view.form-control.form-control-lg.mb-2.input-auth").send_keys("sjwd5407")
    driver.find_element_by_class_name("btn-submit").click()
    dir = f'./{folder}'
    fail_list = []
    if os.path.exists(dir):
        pass
    else:
        os.makedirs(dir)
    for item in stockList:
        try:
            # print('stock: ',item)
            WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.ID, "ember19")))
            input_element = driver.find_element_by_id("ember19")
            input_element.send_keys(item)
            input_element.send_keys(Keys.RETURN)
            driver.execute_script("document.body.style.zoom='50%'")
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "周")]')))
            link = driver.find_element_by_xpath('//button[contains(text(), "周")]')
            driver.execute_script("arguments[0].click();", link)
            thread_element = driver.find_element_by_xpath('//div[@class="legend-ma"]')
            short = float(thread_element.text.split('短多線:', 1)[1].split(' ')[0])
            middle = float(thread_element.text.split('中多線:', 1)[1].split(' ')[0])
            time.sleep(2)
            if middle * 0.93 <= short <= middle * 1.07:
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "月")]')))
                link = driver.find_element_by_xpath('//button[contains(text(), "月")]')
                driver.execute_script("arguments[0].click();", link)
                time.sleep(2)
                element = driver.find_element_by_xpath('//span[@class="custom-control-description blue"]')
                pl = float((element.text).split('%')[0].split(':')[1])
                thread_element = driver.find_element_by_xpath('//div[@class="legend-ma"]')
                short = float(thread_element.text.split('短多線:', 1)[1].split(' ')[0])
                middle = float(thread_element.text.split('中多線:', 1)[1].split(' ')[0])
                time.sleep(2)
                if pl < 65 and middle * 0.93 <= short <= middle * 1.07:
                    driver.get_screenshot_as_file(f'{dir}/{item}.png')
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "ember19")))
            driver.find_element_by_id("ember19").clear()
        except WebDriverException:
            temp = stockList.index((item))
            new_list = stockList[temp:]
            print('start new because fail',item)
            open_fugle(new_list)
        except:
            fail_list.append(item)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "ember19")))
            driver.find_element_by_id("ember19").clear()
    with open('fail.txt','w') as file:
        file.write(fail_list)
        print('fail_list, ',fail_list)

if __name__ == "__main__":
    st_list = goodinfo()
    open_fugle(st_list)