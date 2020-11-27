import requests
from requests_html import HTMLSession

def lr_prediction(se, stock_symbol):
    def fetch_stock_data(symbol, from_Date, end_Date):
        url = "https://www.vndirect.com/portal/thong-ke-thi-truong-chung-khoan/lich-su-gia.shtml"
        try:
            session = HTMLSession()
            response = session.get(url)
        except requests.exceptions.RequestException as e:
            print(e)
