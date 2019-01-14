資策會課程分析網頁
===

# 說明

使用scrapy及data_script進行爬取清理，最後以highchart圖表呈現在網頁，快速了解熱門課程、認證，程式語言以及主題熱門度等資訊。


# 如何設置

1. 設置資料庫

加入Database設置至`my_settings.py`中。

`web_iiiedu/my_settings.py`

```

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '3306',
    }
}

```

2. 安裝依賴

參考requirements.txt進行安裝。


# 如何運行

1. 同步數據庫

```
python manage.py makemigrations
python manage.py migrate
```

2. 運行腳本

```
python manage.py runserver 0.0.0.0:8000
```


# 運行結果

Demo地址：
https://iiiedu.herokuapp.com/iiiedu/chert/theme/

圖

![](https://i.imgur.com/DTkYgoe.png)

