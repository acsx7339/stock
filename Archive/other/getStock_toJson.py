import twstock_downloader
import twstock
from twstock import Stock

# twstock_downloader.get(filepath='/Users/fachu/Desktop/python_test/result.json')
# print(twstock.codes)
# stock = Stock('2330')
# stock.fetch_from(2015, 1)

# with open('./current_data', 'w') as f:
#     f.write(str(twstock.codes))
#     f.close()

num = Stock.fetch_from(2020, 10)
