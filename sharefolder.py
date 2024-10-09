from FinMind.data import DataLoader
from datetime import datetime, timedelta
import pandas as pd
import requests

class Finmind:

    def __init__(self):
        self.api = DataLoader()
        self.api.login_by_token(api_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlIjoiMjAyNC0xMC0wMyAxNToyNjowNiIsInVzZXJfaWQiOiJhY3N4NzMzOSIsImlwIjoiMTExLjI0MC4wLjE2In0.A--Yfs6Iyi6Dj6sxnDYJn6quYdyYY-qKWAh1-2jrMBI')
        self.url = "https://api.finmindtrade.com/api/v3/data"
        self.today = datetime.today()
        
    def GetShareFolder(self, item, date):
        parameter = {
            "dataset": "TaiwanStockHoldingSharesPer",
            "stock_id": item,
            "date": date,
        }
        data = requests.get(self.url, params=parameter)
        data = data.json()
        data = pd.DataFrame(data['data'])
        total_seven = data.head(8)
        print(data.head(8))
        total_percent = total_seven['percent'].sum()
        # print(total_percent)
        return(total_percent)

    # 定義函數來取得最近的星期五
    def get_last_friday(slef, reference_date):
        # 如果今天還沒到星期五（小於星期五的索引值4），往前推到上個星期五
        if reference_date.weekday() < 4:
            days_since_friday = 7 + (reference_date.weekday() - 4)
        else:
            # 否則直接取得最近的星期五
            days_since_friday = reference_date.weekday() - 4
        return reference_date - timedelta(days=days_since_friday)
    
    def get_fridays(self):
        # 取得今天的日期
        today = datetime.today()
        # 取得上週五
        friday = self.get_last_friday(today)
        # 取得上上週五
        previous_friday = friday - timedelta(weeks=1)
        # 格式化日期為 YYYY-MM-DD
        friday_str = friday.strftime('%Y-%m-%d')
        previous_friday_str = previous_friday.strftime('%Y-%m-%d')
        return friday_str, previous_friday_str
    
    def Revenue(self, item):
        today = datetime.today()
        prev_day = (datetime.today() - timedelta(days=30))
        date = [today, prev_day]
        # print(today, prev_day)
        revenue_in_billions_list = []
        for day in date:
            start_date = (day - timedelta(395))
            # print(start_date)
            df = self.api.taiwan_stock_month_revenue(
                stock_id=item,
                start_date=start_date.strftime('%Y-%m-%d'),
                )
            total_revenue = df['revenue'].head(12).sum()
            revenue_in_billions = round(total_revenue / 1e9, 2)
            revenue_in_billions_list.append(revenue_in_billions)
        # 計算兩個營收的差異
        revenue_difference = revenue_in_billions_list[0] - revenue_in_billions_list[1]
        # print(f"這個月的近十二個月營收總和減去上個月的近十二個月營收總和: {revenue_difference} 億")
        if revenue_difference > 0:
            print("revenus is positive")
            return True

    def ratio_result(self, item):
        now_data, previous_date = self.get_fridays()
        # print(now_data, previous_date)
        now_ratio = self.GetShareFolder(item, now_data)
        previous_ratio = self.GetShareFolder(item, previous_date)
        # print(now_ratio, previous_ratio)
        if now_ratio - previous_ratio < 0 and now_ratio < 50:
            print("散戶減少")
            return True
        else:
            print("散戶增加")

if __name__ == "__main__":
    fm = Finmind()
    fm.ratio_result("4426")
    # fm.Revenue("2406")


