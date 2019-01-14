scrapy_iiiedu
---


# 說明

以scrapy爬取資策會網站，同時選擇MongoDB存取資料，方便後續資料整理。

- 爬取網址

    [資策會 職訓課程](https://www.taiwanjobs.gov.tw/internet/index/CourseQuery_step.aspx)
    
    ![](https://i.imgur.com/o3iVH7q.png)


# 如何設置

**設置資料庫**

在scrapy_iiiedu目錄下新增一個my_settings.py，填下真實的資料庫信息，並依照下面的格式填入。

`scrapy_iiiedu/my_settings.py`

```

MONGODB_SERVER = ""
MONGODB_DB = "course"
MONGODB_COLLECTION_IIIEDU = "iiiedu"
MONGODB_COLLECTION_UPLIST = "uplist_iiiedu"

```

# 如何運行

1. 切換目錄

    ```
    cd scrapy_iiiedu
    ```

2. 運行腳本

    ```
    python entrypoint.py
    ```


# 運行結果

**儲存格式**

```
{
    "Class_ID": "MSA384I1801",
    "Class_Name": "Big Data資料處理-Spark實作",
    "Class_address": {
      "unit": "科技化服務訓練中心",
      "city": "高雄",
      "address": "高雄市前金區中正四路211號8F-1"
    },
    "Price_Ownpay": "9000",
    "Training_StartDate": "2018-05-19 00:00:00",
    "Training_EndDate": "2018-05-20 00:00:00",
    "Training_Hours": 12,
    "Course_content": "1.Big Data概述\n-Big Data簡介\n-Big Data平台的介紹與比較 - Hadoop與Spark\n\n2.Hadoop HDFS與Spark安裝\n-在3台linux上安裝Hadoop HDFS分散式儲存系統\n-HDFS指令操作?\n-在HDFS架構上手動安裝Spark Cluster（1台Master + 3台Worker）\n\n3.Spark不同執行模式的操作與使用\n-Spark Local模式的操作\n-Spark Standalone Cluster模式的操作\n-透過spark-shell、pyspark、spark-submit在Spark Cluster上執行scala、python或jar檔\n-IPython Notebook安裝與執行Python Spark（pyspark）程式\n\n4.RDD的操作\n-RDD的轉換（transformation）與動作（action）\n-RDD key-value的基本操作\n-在Spark Cluster上撰寫WordCount並執行\n\n5.Spark SQL、MLlib ALS推薦演算法\n-RDD、DataFrame與Spark SQL的轉換與操作\n-Pandas DataFrame繪圖範例\n\n6.SparkR安裝\n-R、RStudio的安裝\n-SparkR範例練習（讓R執行在Spark Cluster上）",
    "link": "https://w3.iiiedu.org.tw/coursedetail.php?id=MSA384I&l=12&c=MSA384I1801",
    "source": "資策會"
  }
```
