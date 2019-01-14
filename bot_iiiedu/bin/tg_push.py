

from bot_iiiedu.myhelper import conf,MongoHelper
import telegram
from time import sleep

iiedu_push = MongoHelper(**conf.MongoDB_uplist_iiiedu)

total = iiedu_push.collection.find({})


bot = telegram.Bot(token=conf.Telegram_bot['token'])

for item in total:
    TG_text = (
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
    # print(TG_text)
    bot.sendMessage(chat_id=conf.Telegram_bot['chat_id'], text=TG_text)
    sleep(30)
    iiedu_push.collection.delete_one({"_id": item["_id"]})
