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
    new_list = []
    for i in range(0,3):
        while True:
            try:
                if len(new_list) > 1:
                    stockList = new_list
                chrome_options = Options()
                # chrome_options.add_argument('--headless')
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
                time.sleep(20)
                driver.find_element_by_css_selector(("[class='ember-text-field ember-view form-control form-control-lg mb-2']")).send_keys("0938922392")
                driver.find_element_by_class_name("btn-submit").click()
                time.sleep(1)
                driver.find_element_by_class_name("ember-text-field.ember-view.form-control.form-control-lg.mb-2.input-auth").send_keys("sjwd5407")
                driver.find_element_by_class_name("btn-submit").click()
                dir = f'./{folder}'
                if os.path.exists(dir):
                    pass
                else:
                    os.makedirs(dir)
                for item in stockList:
                    WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.ID, "ember19")))
                    input_element = driver.find_element_by_id("ember19")
                    input_element.send_keys(item)
                    input_element.send_keys(Keys.RETURN)
                    driver.execute_script("document.body.style.zoom='50%'")
                    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "周")]')))
                    link = driver.find_element_by_xpath('//button[contains(text(), "周")]')
                    driver.execute_script("arguments[0].click();", link)
                    thread_element = driver.find_element_by_xpath('//div[@class="legend-ma"]')
                    short = float(thread_element.text.split(' ')[0].split(':')[1])
                    middle = float(thread_element.text.split(' ')[2].split(':')[1])
                    time.sleep(2)
                    if middle * 0.93 <= short <= middle * 1.07:
                        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "月")]')))
                        link = driver.find_element_by_xpath('//button[contains(text(), "月")]')
                        driver.execute_script("arguments[0].click();", link)
                        time.sleep(2)
                        element = driver.find_element_by_xpath('//span[@class="custom-control-description blue"]')
                        pl = float((element.text)[6:12])
                        thread_element = driver.find_element_by_xpath('//div[@class="legend-ma"]')
                        short = float(thread_element.text.split(' ')[0].split(':')[1])
                        middle = float(thread_element.text.split(' ')[2].split(':')[1])
                        time.sleep(2)
                        if pl < 65 and middle * 0.93 <= short <= middle * 1.07:
                            driver.get_screenshot_as_file(f'{dir}/{item}.png')
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "ember19")))
                    driver.find_element_by_id("ember19").clear()                    
            except:
                temp = stockList.index((item))
                new_list = stockList[temp:]
                print(new_list)
                continue
            break


if __name__ == "__main__":
    # st_list = goodinfo()
    st_list = ['0050', '0052', '0061', '1101', '1104', '1213', '1215', '1216', '1217', '1218', '1225', '1227', '1229', '1233', '1235', '1236', '1301', '1303', '1308', '1310', '1312', '1313', '1314', '1316', '1323', '1326', '1339', '1340', '1341', '1342', '1410', '1414', '1416', '1417', '1418', '1423', '1432', '1434', '1435', '1437', '1439', '1440', '1441', '1443', '1444', '1447', '1449', '1453', '1459', '1463', '1473', '1474', '1504', '1506', '1512', '1513', '1517', '1528', '1529', '1536', '1540', '1569', '1582', '1604', '1605', '1609', '1612', '1614', '1615', '1616', '1618', '1626', '1707', '1709', '1711', '1713', '1717', '1718', '1720', '1723', '1724', '1725', '1727', '1730', '1731', '1737', '1742', '1781', '1785', '1796', '1799', '1802', '1805', '1808', '1809', '1810', '1813', '1817', '1903', '1906', '2002', '2009', '2010', '2013', '2015', '2025', '2049', '2059', '2064', '2065', '2066', '2204', '2207', '2208', '2235', '2243', '2301', '2303', '2305', '2317', '2321', '2323', '2324', '2330', '2332', '2337', '2340', '2342', '2347', '2349', '2354', '2355', '2356', '2358', '2359', '2365', '2367', '2371', '2377', '2380', '2382', '2383', '2395', '2402', '2408', '2413', '2414', '2417', '2419', '2420', '2421', '2423', '2425', '2426', '2427', '2443', '2444', '2449', '2450', '2451', '2454', '2456', '2459', '2461', '2464', '2465', '2471', '2478', '2480', '2483', '2484', '2489', '2491', '2493', '2495', '2497', '2504', '2505', '2506', '2511', '2515', '2520', '2524', '2536', '2537', '2538', '2539', '2543', '2548', '2601', '2607', '2608', '2611', '2616', '2618', '2630', '2633', '2643', '2704', '2705', '2712', '2719', '2723', '2731', '2740', '2743', '2745', '2748', '2752', '2754', '2755', '2809', '2823', '2832', '2841', '2845', '2849', '2850', '2852', '2867', '2880', '2881', '2882', '2885', '2888', '2890', '2891', '2892', '2897', '2901', '2905', '2908', '2915', '2924', '2928', '2929', '2936', '3004', '3013', '3017', '3022', '3024', '3027', '3029', '3033', '3037', '3038', '3040', '3041', '3043', '3046', '3047', '3048', '3052', '3054', '3058', '3060', '3062', '3066', '3067', '3081', '3083', '3089', '3092', '3105', '3115', '3118', '3122', '3128', '3131', '3141', '3152', '3164', '3176', '3178', '3191', '3205', '3211', '3213', '3217', '3226', '3228', '3229', '3232', '3257', '3264', '3268', '3276', '3288', '3289', '3303', '3310', '3311', '3312', '3313', '3324', '3325', '3332', '3356', '3360', '3379', '3383', '3416', '3426', '3432', '3443', '3444', '3450', '3454', '3465', '3479', '3484', '3489', '3490', '3498', '3499', '3516', '3520', '3521', '3522', '3523', '3529', '3537', '3540', '3541', '3546', '3552', '3556', '3557', '3564', '3567', '3570', '3576', '3583', '3587', '3588', '3593', '3607', '3615', '3617', '3623', '3628', '3629', '3652', '3661', '3669', '3682', '3684', '3694', '3703', '3711', '4102', '4104', '4106', '4111', '4114', '4116', '4123', '4130', '4138', '4139', '4142', '4152', '4154', '4157', '4160', '4164', '4183', '4188', '4304', '4306', '4413', '4419', '4420', '4426', '4429', '4439', '4529', '4530', '4535', '4538', '4542', '4543', '4545', '4549', '4550', '4554', '4556', '4557', '4564', '4568', '4572', '4580', '4609', '4706', '4716', '4721', '4741', '4744', '4747', '4754', '4755', '4760', '4764', '4767', '4803', '4806', '4903', '4908', '4912', '4915', '4916', '4919', '4924', '4927', '4935', '4939', '4943', '4953', '4960', '4971', '4973', '4977', '4979', '4991', '4994', '4995', '4999', '5009', '5011', '5201', '5203', '5205', '5206', '5213', '5220', '5223', '5230', '5234', '5245', '5263', '5269', '5272', '5276', '5281', '5284', '5287', '5288', '5301', '5302', '5309', '5314', '5340', '5345', '5347', '5348', '5356', '5371', '5383', '5386', '5388', '5398', '5403', '5432', '5434', '5438', '5450', '5455', '5460', '5469', '5471', '5475', '5481', '5487', '5489', '5490', '5493', '5498', '5511', '5515', '5520', '5521', '5522', '5523', '5531', '5534', '5536', '5538', '5603', '5604', '5607', '5701', '5704', '5820', '5871', '5876', '5880', '5902', '5903', '5906', '6005', '6015', '6016', '6020', '6021', '6026', '6101', '6103', '6104', '6111', '6117', '6118', '6125', '6130', '6134', '6138', '6141', '6147', '6148', '6154', '6160', '6161', '6163', '6166', '6169', '6171', '6172', '6177', '6179', '6180', '6183', '6196', '6198', '6203', '6206', '6208', '6210', '6212', '6213', '6214', '6215', '6217', '6219', '6220', '6221', '6222', '6228', '6233', '6236', '6239', '6241', '6242', '6243', '6244', '6247', '6251', '6259', '6265', '6266', '6274', '6276', '6281', '6289', '6291', '6292', '6294', '6409', '6412', '6415', '6416', '6417', '6418', '6419', '6425', '6438', '6446', '6449', '6451', '6456', '6462', '6465', '6482', '6485', '6486', '6491', '6505', '6506', '6515', '6523', '6535', '6541', '6548', '6556', '6570', '6574', '6576', '6577', '6588', '6590', '6594', '6598', '6603', '6615', '6624', '6629', '6640', '6642', '6654', '6661', '6662', '6664', '6674', '6680', '6683', '6706', '6728', '6732', '6733', '6751', '6752', '6756', '6762', '6776', '6781', '8011', '8027', '8028', '8033', '8043', '8046', '8047', '8048', '8049', '8050', '8054', '8064', '8070', '8083', '8084', '8085', '8086', '8091', '8096', '8097', '8099', '8101', '8104', '8105', '8109', '8121', '8155', '8163', '8201', '8222', '8234', '8240', '8249', '8271', '8277', '8284', '8289', '8291', '8342', '8390', '8403', '8410', '8411', '8418', '8422', '8423', '8424', '8426', '8427', '8431', '8433', '8443', '8455', '8467', '8473', '8476', '8477', '8478', '8489', '8499', '8906', '8917', '8926', '8927', '8928', '8930', '8931', '8932', '8935', '8936', '8940', '8941', '8942', '9902', '9907', '9910', '9917', '9926', '9935', '9937', '9940', '9944', '9945', '9949', '9950', '9960']
    open_fugle(st_list)