# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import requests


def get_series_data(url, theme):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
    }

    web = requests.get(url, headers=header)

    # 編碼
    web.encoding = 'big5'

    soup = BeautifulSoup(web.text, "lxml")

    # soup = BeautifulSoup(web_text.text.encode('big5').decode('utf8'),"lxml")
    title = soup.select("p > font")
    # print(title)

    trs = soup.select("table  tr")
    # print("trs",len(trs))

    ths = [
        '課程領域', '課程名稱', '開始日期', '結束日期', '時數', '上課時段', '優惠方案'
    ]

    ret = []
    t1 = ""

    for tds in trs:
        tds = tds.select("td")
        if len(tds) == 1:

            t1 = tds[0].text.strip()
            # print(t1)
            # print(td[0]['rowspan'])
        elif t1:

            name = tds[1].text.strip()

            if name:
                data = {'name': name, 'series': t1, 'theme': theme}

                ret.append(data)

    # result = {theme: ret}
    return ret


# "http://www.iiiedu.org.tw/ites/type1.htm"




def main():
    theme = [
        {"theme": "資訊架構規劃", 'url': "http://www.iiiedu.org.tw/ites/type1.htm"},
        {"theme": "資訊系統開發", 'url': "http://www.iiiedu.org.tw/ites/type2.htm"},
        {"theme": "大數據 / AI", 'url': "http://www.iiiedu.org.tw/ites/type3.htm"},
        {"theme": "數位行銷", 'url': "http://www.iiiedu.org.tw/ites/type4.htm"},
        {"theme": "智慧產業", 'url': "http://www.iiiedu.org.tw/ites/type5.htm"},
        {"theme": "科技創新管理", 'url': "http://www.iiiedu.org.tw/ites/type6.htm"},
        {"theme": "軟實力", 'url': "http://www.iiiedu.org.tw/ites/type7.htm"},
    ]

    data = list(map(lambda x: get_series_data(**x), theme))
    # print(data)
    # type1 = get_series_data("http://www.iiiedu.org.tw/ites/type1.htm")
    # print(type1)
    data = [n for row in data for n in row]

    return (data)


