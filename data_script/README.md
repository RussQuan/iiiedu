簡單資料清理
===


# 說明

data_script裡面的腳本是用來清理及整理資料，將一開始由scrapy爬取到的在做二次加工。


## 如何設置

1. 設定資料庫

在myhelper目錄下新增一個conf.py，填下真實的資料庫信息，並依照下面的格式填入。

`myhelper/conf.py`


```

MongoDB_iiiedu = {
    'host':'',
    'db_name':'course',
    'collection':'iiiedu'

}

MongoDB_Temp = {
    'host':'',
    'db_name':'course',
    'collection':'temp'

}

MongoDB_Chart = {
    'host':'',
    'db_name':'course',
    'collection':'chart'

}

```

2. 資料庫結構說明

- MongoDB_iiiedu
    
    放置爬取到的歷史資料，以MongoDB爬取方便二次加工。
    
    ![](https://i.imgur.com/JiwXRoY.jpg)
    
    
- MongoDB_Temp
    
    由BS4進行六大主題的爬取，同時對照'MongoDB_iiiedu'進行配對分類，再新增到`MongoDB_Temp`。
    
    ![](https://i.imgur.com/zHgLnQE.jpg)
    
    
- MongoDB_Chart

    根據`MongoDB_iiiedu`,`MongoDB_Temp`這兩個集合，進行三個十大加上六大主題的運算，直接將highchart js參數新增到`MongoDB_Chart`。
    
    ![](https://i.imgur.com/d2UVJET.png)
    


## 如何運行

bin目錄下每個py都可以運行，分別作用如下

- 1、2、3、4 是對iiiedu該集合進行更新優化。

- 5 是以iiiedu再將資料規整化到Mysql，由於該腳本mysql是讀取Django ORM的關係，因此需要先同步Django資料庫在執行此腳本。

- 6 是以bs4爬取到的內容過濾新增到`MongoDB_Temp`。

- 7 是直接將三個十大加上六大主題的highchart js新增到`MongoDB_Chart`。

1. 切換目錄

```
cd data_script/bin
```

2. 運行腳本

```
python 1. 資料分類.py
python 2. 地址優化.py
python 3. 十大語言.py
python 4. sync_django_datal.py
python 5. 補上十大語言.py
python 6. bs4_plus.py
python 7. up_chart_mongo.py
```



