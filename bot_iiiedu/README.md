TeleGram Bot Send
===


# 說明

bot_iiiedu為機器人腳本目錄，目前只有發送功能。主要實現是先透過scrapy爬取後會同時儲存在`iiiedu`、`uplist_iiiedu`這兩個集合中，由於`iiiedu`為主要歷史集合，因此`uplist_iiiedu`為發送集合，每次機器人發送前會先遍歷集合，而在每發送一次就會刪除一筆資料。


## 如何使用

1. 設定資料庫

> myhelper/conf.py

```


MongoDB_uplist_iiiedu = {
    'host':'',
    'db_name':'course',
    'collection':'iiiedu'

}

Telegram_bot = {
    'token':'',
    'chat_id':''
}


```

2. 資料庫結構說明

- MongoDB_uplist_iiiedu

    放置發送待發送的資料，由scrapy新增，bot發送後刪除。
    

- Telegram_bot

    放置機器人的token以及頻道/群組的chat_id。


## 如何運行

1. 切換目錄

```
cd bot_iiiedu/bin
```

2. 運行腳本

```
python bin/tg_push.py
```


# 運行結果

**課程頻道**

![](https://i.imgur.com/wc3uNXp.png)



