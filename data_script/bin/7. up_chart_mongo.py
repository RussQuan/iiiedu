import pandas as pd
from myhelper import MongoHelper,Highchart_Helper,export_pkl,conf
import json

# 匯出
export_pkl(conf.MongoDB_iiiedu,'iiiedu.pkl')
export_pkl(conf.MongoDB_Temp,'dfiii_temp.pkl')


# 獲取初始資料
dfiii = pd.read_pickle('iiiedu.pkl')
dfiii_temp = pd.read_pickle('dfiii_temp.pkl')


# --- 10大語言班
lang = ["Python","C語言","Java","C+\+","C#","R","JavaScript","PHP","Go","Swift"]
dfiii_lang = dfiii[~dfiii.lang.isnull()]

# ---  10大認證班
# 篩選認證班
dfiii_certified = dfiii[dfiii.cate.map(lambda x: x in ["認證"])]

# ---  10大課程(排除"養成班","認證班")

dfiii_Class = dfiii[dfiii.cate.map(lambda x: x not in ["認證", "養成班"])]



# --- 主題

# print(dfiii_temp)



# --- 系列領域


# 2. 系列領域
#
# s = dftheme.apply(lambda x: pd.Series(x['series']), axis=1).stack().reset_index(level=1, drop=True)
# s.name = 'series'
# dftheme2 = dftheme.drop('series', axis=1).join(s)

# 3. 遍歷series

'''
大數據 / AI = BDAI
數位行銷 = DM
智慧產業 = WI #"wisdom industry"
科技創新管理 = TIM #Technology Innovation Management
資訊架構規劃 = IAP #Information Architecture Planning
資訊系統開發 = ISD #Information System Development
軟實力 = SW #Soft power
'''

dfAI = dfiii_temp[dfiii_temp['theme'].map(lambda x: x in "大數據 / AI")]
dfDM = dfiii_temp[dfiii_temp['theme'].map(lambda x: x in "數位行銷")]
dfWI = dfiii_temp[dfiii_temp['theme'].map(lambda x: x in "智慧產業")]
dfTIM = dfiii_temp[dfiii_temp['theme'].map(lambda x: x in "科技創新管理")]
dfIAP = dfiii_temp[dfiii_temp['theme'].map(lambda x: x in "資訊架構規劃")]
dfISD = dfiii_temp[dfiii_temp['theme'].map(lambda x: x in "資訊系統開發")]
dfSW = dfiii_temp[dfiii_temp['theme'].map(lambda x: x in "軟實力")]


def series_data(df):
    H = Highchart_Helper(df)
    H.col = "series"
    H.ycol = "Training_StartM"
    return H.ret_chart()



# df to json
topclass = Highchart_Helper(dfiii_Class).ret_chart()
topcert = Highchart_Helper(dfiii_certified).ret_chart()
toplang = Highchart_Helper(dfiii_lang).ret_chart()

# theme
H = Highchart_Helper(dfiii_temp)
H.col = "theme"
H.ycol = "Training_StartM"
totheme = H.ret_chart()


mongo = MongoHelper(**conf.MongoDB_Chart)

mongo.collection.drop()
mongo.collection.insert_one({"chart":"class","data":topclass})
mongo.collection.insert_one({"chart":"cert","data":topcert})
mongo.collection.insert_one({"chart":"lang","data":toplang})
mongo.collection.insert_one({"chart":"theme","data":totheme})

mongo.collection.insert_one({"chart":"ai","data":series_data(dfAI)})
mongo.collection.insert_one({"chart":"dm","data":series_data(dfDM)})
mongo.collection.insert_one({"chart":"wi","data":series_data(dfWI)})
mongo.collection.insert_one({"chart":"tim","data":series_data(dfTIM)})
mongo.collection.insert_one({"chart":"iap","data":series_data(dfIAP)})
mongo.collection.insert_one({"chart":"isd","data":series_data(dfISD)})
mongo.collection.insert_one({"chart":"sw","data":series_data(dfSW)})

