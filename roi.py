from fugle_marketdata import RestClient

client = RestClient(api_key = 'C34DFA55B7134857')  # 輸入您的 API key
stock = client.stock  # Stock REST API client

item = stock.historical.candles(**{"symbol": "0050", "from": "2023-02-06", "to": "2023-02-08", "fields": "open,high,low,close,volume,change"})
print(item)