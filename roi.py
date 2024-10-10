from fugle_marketdata import RestClient

client = RestClient(api_key = 'NTFhZTU0YzItZDk2OC00YTI \
                    1LWE0YWQtZDhmNjVlZjA2YTY4IDFjMjkyMm \
                    JjLWYwNDktNDlmZi1hZWM2LTU4ZmYyZWEzMDE3Zg')  # 輸入您的 API key
stock = client.stock  # Stock REST API client

stock_item = ['1231', '1466', '2015', '2103', '2115', 
              '2362', '2402', '2419', '2426', '2480', 
              '2727', '3209', '3447', '3494', '3533', 
              '4557', '4807', '4930', '4935', '6415', 
              '6805', '6807', '8028', '8201', '9924']
for item in stock_item:
    data = stock.historical.candles(**{"symbol": item, "fields": "close"})
    # print(data)
    first_item = data['data'][0]
    first_date = first_item['date']
    first_close = first_item['close']
    print(f"stock: {item}, close price is : {first_close}")