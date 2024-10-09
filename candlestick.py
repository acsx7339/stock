import talib
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
from GetTWStock import TWStock
from scipy.signal import find_peaks


class Yfinance:

    def __init__(self):
        self.end_date = pd.Timestamp(datetime.now()).normalize() + pd.offsets.MonthEnd(0)
        self.start_date = self.end_date - pd.DateOffset(months=60)
        # print(f"start date: {self.start_date.date()}, end date: {self.end_date.date()}")

    def yahoo_result(self, stock):
        content = yf.download(f'{stock}.TW', start=self.start_date, end=self.end_date)
        return content
    
    def monthly_status(self, content):
        monthly_stock = content['Adj Close'].resample('ME').last()
        monthly_stock = monthly_stock.dropna()
        monthly_stock = monthly_stock.astype(float)
        monthly_stock_df = pd.DataFrame(monthly_stock)
        monthly_stock_df['5MA'] = talib.SMA(monthly_stock_df['Adj Close'].values.astype(float), timeperiod=5)
        monthly_stock_df['10MA'] = talib.SMA(monthly_stock_df['Adj Close'].values.astype(float), timeperiod=10)
        # print(monthly_stock_df[['5MA', '10MA']].tail(2))
        return monthly_stock_df[['5MA', '10MA']].tail(2)

    def daily_status(self, content):
        daily_stock = content['Adj Close']
        daily_stock = daily_stock.dropna()
        daily_stock = daily_stock.astype(float)
        daily_stock_df = pd.DataFrame(daily_stock)
        daily_stock_df['5MA'] = talib.SMA(daily_stock_df['Adj Close'].values.astype(float), timeperiod=5)
        daily_stock_df['10MA'] = talib.SMA(daily_stock_df['Adj Close'].values.astype(float)-0.2, timeperiod=10)
        daily_stock_df['60MA'] = talib.SMA(daily_stock_df['Adj Close'].values.astype(float), timeperiod=60)
        # print(daily_stock_df[['5MA', '10MA', '60MA']].tail(2))
        return daily_stock_df[['5MA', '10MA', '60MA']].tail(2)

    def upper_trend(self, item, ma):
        cur_date = item.index[1].strftime('%Y-%m-%d')
        prev_date = item.index[0].strftime('%Y-%m-%d')
        cur_ma = item.loc[cur_date, ma]
        prev_ma = item.loc[prev_date, ma]
        print(f"current {ma} value is {cur_ma}, previous value is {prev_ma}")
        upper_result = cur_ma - prev_ma
        if upper_result > 0:
            print(f"{ma} is upper trend")
            return True
        else:
            print(f"{ma} is down trend")
        

    def high_trend(self, item):
        cur_date = item.index[1].strftime('%Y-%m-%d')
        value_5ma = item.loc[cur_date, "5MA"]
        value_10ma = item.loc[cur_date, "10MA"]
        result_ma = value_5ma - value_10ma
        if value_10ma * 1.08 > value_5ma  and result_ma > 0:
            print(f"5ma is bigger than 10ma and within 1.08%")
            return True
        elif value_10ma * 1.08 < value_5ma:
            print(f"5ma is far from 10ma")
        elif value_10ma > value_5ma:
            print("10ma value is greater than 5ma")

    def volume_break(self, item):
        daily_volume = item['Volume'] // 1000
        recent_volume = daily_volume.tail(21)
        high_volumes_21 = recent_volume.max()
        current_volume = recent_volume.iloc[-1]
        # print(high_volumes_21, current_volume)
        if current_volume > high_volumes_21:
            print("today volume is higher than recent 21 days volume")
            return True
        else:
            print("volume is not higher than previosu")
        
    def price_break(self, item):
        high_prices = item.tail(21)['High'].values
        peaks, _ = find_peaks(high_prices)
        if len(peaks) > 0:
            print("局部高点的日期和价格:")
            highest_peak_idx = peaks[np.argmax(high_prices[peaks])]
            print("最高局部高点的日期和价格:")
            print(item.tail(21).index[highest_peak_idx], high_prices[highest_peak_idx])
        else:
            print("没有找到局部高点")
        cur_close = item['Close'][-1]
        # print(cur_close)
        if cur_close > high_prices[highest_peak_idx]:
            return True 
        else:
            print("price is not higher than previous")

        
# if __name__ == "__main__":
    # stock = Yfinance()
    # content = stock.yahoo_result("2102")
    # stock.price_break(content)
    # print(content)
    # stock.volume(content)
    # item = stock.monthly_status(content)
    # stock.upper_trend(item, "5MA")
    # stock.high_trend(item)
