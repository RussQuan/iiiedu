# -*- coding: utf-8 -*-

import scrapy
import re
import datetime


class getSpider(scrapy.Spider):
    name = "iiiedu"

    # 偽裝頭部
    '''
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
        "Connection": "keep-alive",
        "Content-Type": " application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Referer": " http://www.iiiedu.org.tw/",
    }
    '''

    start_urls = ["https://w3.iiiedu.org.tw/LongTerm.php",
                  "https://w3.iiiedu.org.tw/holidayclass.php",
                  "https://w3.iiiedu.org.tw/Identify.php",
                  "https://w3.iiiedu.org.tw/rentclass.php",
                  ]

    allowed_domains = ["w3.iiiedu.org.tw"]  # 可選
    download_delay = 2  # 减慢爬取速度 为2s

    def parse(self, response):

        pages = len(response.xpath(".//select/option"))

        for page in range(1, pages):
            t = response.xpath("string(.//form[@name='PageChange']/input//@value)").extract()[0]
            # print(t)
            newurl = "{url}?token={t}&Page={num}".format(url=response.url, t=t, num=page)
            request = scrapy.Request(newurl, callback=self.parse_list)
            yield request

        '''
        request = scrapy.Request(ths["class_link"],
                                 callback=self.parse_2,
                                 meta={"date": ths["date"],
                                       "class_id": ths["class_id"],
                                       "class_add": ths["class_location"],
                                       "class_period": ths["class_period"],
                                       "class_name": ths["class_name"]
                                       },
                                 dont_filter=True)
        yield request
        '''

    def parse_list(self, response):

        print(response.url)
        tables = response.xpath(".//*[@class='listing']//tr")

        # ths = ["課程名稱","開課日期","結束日期","開課中心","地點","定價","優惠價","時數"]

        thlists = [
            {
                "name": "課程名稱",
                "status": True,
                "set": {
                    "Class_Name": ".//text()",
                    "Class_Link": ".//@href"
                }

            },
            {
                "name": "開課日期",
                "status": True,
                "set": {
                    "Training_StartDate": ".//text()",
                }

            },
            {
                "name": "結束日期",
                "status": True,
                "set": {
                    "Training_EndDate": ".//text()",
                }

            },
            {
                "name": "開課中心",
                "status": True,
                "set": {
                    "unit": ".//text()",
                }

            },
            {
                "name": "地點",
                "status": True,
                "set": {
                    "city": ".//text()",
                }

            },
            {
                "name": "定價",
                "status": True,
                "set": {
                    "Price": ".//text()",
                }

            },
            {
                "name": "優惠價",
                "status": True,
                "set": {
                    "Price_Ownpay": ".//text()",
                }

            },
            {
                "name": "時數",
                "status": True,
                "set": {
                    "Training_Hours": ".//text()",
                }

            },

        ]

        result = []
        for i, item in enumerate(tables):
            if i == 0:
                pass
            else:
                tds = item.xpath(".//td")
                data = {}
                for thlist, td in zip(thlists, tds):
                    if thlist["status"]:
                        for k, y in list(thlist["set"].items()):
                            data[k] = "".join(td.xpath(y).extract()).strip()
                    else:
                        pass
                result.append(data)

        for item in result:
            hosturl = "https://w3.iiiedu.org.tw/"
            request = scrapy.Request("{}{}".format(hosturl, item["Class_Link"]),
                                     callback=self.parse_Page,
                                     meta=item,
                                     dont_filter=True)
            yield request

    def parse_Page(self, response):
        print(response.url)

        Class_ID = response.url.split('=').pop()

        # 課程大綱 ,去空格
        Course_content = "\n".join(
            [i.strip() for i in response.xpath(".//*[@id='centerBodyBox']/div/div[6]//text()").extract()])

        # 上课地址

        strall = response.xpath(".//*[@class='detail_content']//text()").extract()
        for s in strall:
            if "上課地址" in s:
                print(s)
                Class_Localtion = s.split('：')[1].strip()
                print(Class_Localtion)

        # 上課時間、上課時段 (20180408)

        # 所有表格
        tableall = response.xpath("..//table//tr")
        for i in tableall:
            strlist = i.xpath(".//text()").extract()
            if Class_ID in strlist:
                # print("ok")
                # print(strlist)
                # 上課時間
                Training_Weekly = strlist[1]
                # print(Training_Weekly)
                # 上課時段
                Training_Period = strlist[2]
                # print(Training_Period)

        '''
        Class_Localtion = response.xpath(".//*[@id='centerBodyBox']/div/div[12]/text()[1]").extract()[0].strip()
        print(Class_Localtion)
        # 上課地址：台北市復興南路一段390號2樓\
        Class_Localtion = Class_Localtion.split('：')[1].strip()
        print(Class_Localtion)
        '''

        item = {
            "Class_ID": Class_ID,
            "Class_Name": response.meta["Class_Name"],
            "Class_address": {
                "unit": response.meta["unit"],
                "city": response.meta["city"],
                "address": Class_Localtion
            },
            "unit": response.meta["unit"],
            "city": response.meta["city"],
            "address": Class_Localtion,

            "Price_Ownpay": "".join(re.findall("\d+", response.meta["Price"])),

            "Training_StartDate": datetime.datetime.strptime(response.meta["Training_StartDate"], "%Y-%m-%d"),
            "Training_EndDate": datetime.datetime.strptime(response.meta["Training_EndDate"], "%Y-%m-%d"),
            "Training_Hours": int(response.meta["Training_Hours"]),
            "Training_Weekly": Training_Weekly,
            "Training_Period": Training_Period,
            "Course_content": Course_content,

            "link": response.url,
            "source": "資策會",
            "create_time": datetime.datetime.now()

        }

        item["TG"] = (
            "課程代碼：{Class_ID}\n"
            "課程名稱：{Class_Name}\n"
            "訓練位置：{Class_address[address]}\n"
            "訓練單位：{Class_address[unit]}\n"
            "學員負擔：{Price_Ownpay}\n"
            "訓練日期：{Training_StartDate} ~ {Training_EndDate}\n"
            "訓練時數：{Training_Hours}小時\n"
            "課程內容：\n{Course_content}\n"
            "課程來源：{source}\n"
            "課程連結：{link}"
        ).format(**item)


        yield item
