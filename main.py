from GetTWStock import TWStock
from sharefolder import Finmind as fm
from candlestick import Yfinance as yf

def main():
    stocklist = TWStock().CODE()
    print(f"stock list is {stocklist}")
    print("-----")
    filter1 = []
    for item in stocklist:
        print("-----")
        print(f"current test stock is {item}")
        stock_content = yf().yahoo_result(item)
        daily_content = yf().daily_status(stock_content)
        Weekly_content = yf().Weekly_status(stock_content)
        if (yf().upper_trend(daily_content, "5MA") and # 只要是往上的就可以
            yf().upper_trend(daily_content, "10MA") and
            yf().upper_trend(daily_content, "60MA") and
            yf().upper_trend(Weekly_content, "5MA") and 
            yf().upper_trend(Weekly_content, "10MA") and
            yf().high_trend(daily_content) and #5ma要比10ma高且不能高超過1.08
            yf().high_trend(Weekly_content) 
            # yf().volume_break(stock_content) and
            # yf().price_break(stock_content)
            ):
            filter1.append(item)
    print(filter1)
    print(f"-------start to filter second times-------")
    filter2 = []
    for target in filter1:
        print(f"current second test stock is {target}")
        print("-----")
        if (fm().ratio_result(target) and
            fm().Revenue(target)          
            ):
            filter2.append(target)
    print(f"final result is {filter2}")

if __name__ == "__main__":
    main()
