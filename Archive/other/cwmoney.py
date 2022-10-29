import requests         #導入requests模組，呼 Http用
import json             #導入json模組
import pandas as pd
import csv
import datetime as datetime
import pandas_datareader as pdr

standard_volume = 1000
one_hundred_day_ago = datetime.timedelta(days = 143)
start_day = datetime.datetime.now() - one_hundred_day_ago
end_day = datetime.datetime.now()
print(start_day, end_day)

def data():
        
    #正式機_帳號設定--------------------------------------------------------------------------------
    appid="20201119233648770"  #APPID
    appsecret="1bfc20302f1c11eb8eaa000c29beef84" #應用程式密鑰

    #正式機_取得交易驗證碼網址----------------------------------------------------------------------
    token_url = "https://owl.cmoney.com.tw/OwlApi/auth"

    #組連線參數------------------------------------------------------------------------------------
    token_params = "appId="+appid+"&appSecret="+appsecret
    token_headers = {'content-type': "application/x-www-form-urlencoded"}  #POST表單，預設的編碼方式 (enctype)
    #取得token------------------------------------------------------------------------------------
    token_res = requests.request("POST", token_url, headers=token_headers, data=token_params)    #請求回覆的狀態 <Response [200]>

    if (token_res.status_code==200):            #若請求http 200(成功)
        token_data=json.loads(token_res.text)   #將token_res的內容，用json.loads()解碼成python編碼
        token=token_data.get("token")           #取token值
        
        #呼叫 data API-------------------------------------------------------------------------------
        data_url="https://owl.cmoney.com.tw/OwlApi/api/v2/json/"
        pid="FAA-14812b"  
        stock_headers = {'authorization': "Bearer "+token}
        stock_res = requests.request("GET", data_url+pid , headers=stock_headers)
        stock_data = json.loads(stock_res.text)
        dfs = pd.DataFrame(stock_data.get("Data"), columns=stock_data.get('Title'))
        dfs = dfs[['股票代號','股票名稱','收盤價', '成交量']]
        dfs.to_csv ('./stock.csv', index = False, header=True)
        

        data_url="https://owl.cmoney.com.tw/OwlApi/api/v2/json/"
        pid="FBA-14820b"  
        major_headers = {'authorization': "Bearer "+token}
        major_res = requests.request("GET", data_url+pid , headers=major_headers)
        major_data = json.loads(major_res.text)
        dfm = pd.DataFrame(major_data.get('Data'), columns=major_data.get('Title'))
        dfm = dfm[['股票代號','股票名稱','主力買賣超(張數)']]
        dfm.to_csv('./major.csv', index=False, header=True)   
        # if (stock_res.status_code==200 and major_res.status_code==200):         
        #     with open('./major.txt', 'a') as f:
        #         f.write(str(stock))
        #         f.write(str(major))
        #         f.close()   
        #     print(data) #顯示資料
        #     return data       
            
        # else:
        #     print("取得資料連線錯誤!"+str(stock_res.status_code))   
            
    else: #無法取得資料時顯示
        print("取得token連線錯誤!"+str(token_res.status_code))

def filter_volume():
    #---volume > 1000
    data = ''
    file = open('./stock.csv')
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        if int(row[3]) >standard_volume:
            data += (row[0])+','
    data = data.split(',')[:-1]
    return data
            

def filter_ratio(code):
    value_list = []
    try:
        stock_number = code+'.TW'
        start = start_day
        end   = end_day
        DataFrame = pdr.DataReader(stock_number, 'yahoo', start, end)
        close_array = DataFrame['Close']
        max_value = round(max(close_array), 2)
        # print(max_value)
        min_value = round(min(close_array), 2)
        # print(min_value)
        current_value = round(close_array[-1], 2)
        # print('target stock: ', code,'max price: ', max_value, 'min price:', min_value, 'current price:', current_value)
        value_list +=[code, current_value, max_value, min_value]
        return(value_list)
    except:
        return None

def price_level(ratio_stock):
    print('ratio stock',ratio_stock)
    watch_stock = ''
    upper_value = (ratio_stock[1] - ratio_stock[3])
    lower_value = (ratio_stock[2] - ratio_stock[3])
    ratio = round(upper_value/lower_value, 2)*100
    if ratio < 65 :
        watch_stock = ratio_stock[0]
        # print(watch_stock)
        return (watch_stock)
    # print('code: ', watch_stock, 'ratio: ', ratio)
    else:
        return None


def major(code):
    print(code)
    id_code = ''
    number = ''
    file = open('./major.csv')
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        id_code +=  row[0]+','
        number += row[2]+','
    id_code = id_code.split(',')[:-1]
    number = number.split(',')[:-1]
    result = dict(zip(id_code, number))
    if int(result.get(code)) > 0:
        return code
    else:
        return ''
    

if __name__ == "__main__":
    result = ''
    ratiotarget_code = ''
    data()
    volume_code = filter_volume()
    # volume_code = ['2368']
    for target_list in volume_code:
        ratio_stock = filter_ratio(target_list)
        if ratio_stock is None :
            pass
        else:
            level_code = price_level(ratio_stock)
        if level_code == None:
            pass
        else:
            final = major(level_code)
            result += (final+',' if final else '')
    result = result.split(',')[:-1]
    # print(ratiotarget_code)
    print('result:' ,result)
