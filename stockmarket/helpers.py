import datetime
import quandl

def get_yesterday_stock_price(ss):
    d = datetime.datetime.today()
    start_date = (d - datetime.timedelta(days=5)).date()
    data = quandl.get("NSE/"+ss+"/CLOSE", start_date=start_date, end_date=d,
                      column_index=1, returns="numpy")
    return round(float(data[-1][1]), 2)