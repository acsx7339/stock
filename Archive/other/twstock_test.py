import twstock
import pandas as pd
import time
import pandas_datareader as pdr
import datetime as datetime
import json
import requests
import csv
import tkinter as tk

def get_all_stock_id():
    code = []
    data = ''
    # link = 'https://quality.data.gov.tw/dq_download_json.php?nid=11549&md5_url=bb878d47ffbe7b83bfc1b41d0b24946e'
    # r = requests.get(link)
    # data = pd.DataFrame(r.json())
    # data.to_csv('./test.csv', index=False, header = True)

    with open('./test.csv', newline='') as d:
        rows = csv.reader(d)
        for row in rows:
            data += str(row[0])+','
        code = (data.split(',', 1)[1]).split(',')[:-1]
        print(code)
        return code
        

def get_100d_data(target_stock):
    stock_number = target_stock+'.TW'
    start = datetime.datetime(2020,7,1)
    end   = datetime.datetime(2020,11,20)
    DataFrame = pdr.DataReader(stock_number, 'yahoo', start, end)
    close_array = DataFrame['Close']
    max_value = max(close_array)
    min_value = min(close_array)
    current_value = close_array[-1]
    print('target stock: ', target_stock,'max price: ', int(max_value), 'min price:', int(min_value), 'current price:', int(current_value))
    return(target_stock, float(current_value), float(max_value), float(min_value))
        
def percentage(stock, curr, max_num, min_num):
    watch_stock = []
    total_ratio = []
    upper_value = (curr - min_num)
    lower_value = (max_num - min_num)
    ratio = int((round(upper_value/lower_value, 2))*100)
    if ratio < 50 and ratio > 30:
        watch_stock.append(stock)
        total_ratio.append(ratio)
    else:
        watch_stock.append("")
        total_ratio.append("")
    print('Percentage: ', ratio)
    return (watch_stock, total_ratio)

def major(stock):
    with open('./test.csv', newline='') as d:
        rows = csv.reader(d)
        for row in rows:
            data += str(row[0])+','
        code = (data.split(',', 1)[1]).split(',')[:-1]
        print(code)
        return code
    

if __name__ == "__main__":

    # target_item = []
    # code_id = get_all_stock_id()
    # for item in code_id:
    #     try:
    #         print(item)
    #         (stock, curr, max_num, min_num) = get_100d_data(item)
    #         (watch_stock, ratio) = percentage(stock, curr, max_num, min_num)
    #         target_item += list(watch_stock)
    #         print(watch_stock, ratio)
    #     except KeyError:
    #         pass
        
    # sort_item = list(filter(None, target_item))
    # print('total stock number is: ', len(sort_item), "\n"'here is the stock content: ', sort_item)
