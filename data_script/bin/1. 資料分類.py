

from myhelper import MongoHelper
from myhelper import conf

import re

mongo = MongoHelper(**conf.MongoDB_iiiedu)

# 做好分類

data = [
    {"key": "CFA", "cate": "數位內容", "tag": "美術類"},
    {"key": "CPG", "cate": "數位內容", "tag": "程式類"},
    {"key": "CPD", "cate": "數位內容", "tag": "企劃類"},
    {"key": "CMU", "cate": "數位內容", "tag": "音樂類"},
    {"key": "CSM", "cate": "數位內容", "tag": "行銷類"},
    {"key": "CMG", "cate": "數位內容", "tag": "管理類"},
    {"key": "CPA", "cate": "數位內容", "tag": "出版類"},
    {"key": "CEL", "cate": "數位內容", "tag": "數位學習類"},
    {"key": "CMA", "cate": "數位內容", "tag": "多媒體應用類"},

    {"key": "SIT", "cate": "科技服務", "tag": "科技應用服務類"},
    {"key": "SEB", "cate": "科技服務", "tag": "企業電子化類"},

    {"key": "MIS", "cate": "管理類型", "tag": "資訊管理服務類"},
    {"key": "MSA", "cate": "管理類型", "tag": "資訊架構類"},
    {"key": "MTI", "cate": "管理類型", "tag": "科技管理類"},
    {"key": "MPM", "cate": "管理類型", "tag": "專案管理類"},

    {"key": "NCN", "cate": "網路類型", "tag": "網路類"},

    {"key": "AOS", "cate": "系統管理", "tag": "作業系統管理類"},
    {"key": "ADB", "cate": "系統管理", "tag": "資料庫系統管理類"},
    {"key": "ASQ", "cate": "系統管理", "tag": "資訊安全系統管理類"},
    {"key": "AOA", "cate": "系統管理", "tag": "辦公室應用類"},

    {"key": "DPR", "cate": "系統開發", "tag": "程式設計類"},
    {"key": "DWB", "cate": "系統開發", "tag": "網頁開發類"},
    {"key": "DEM", "cate": "系統開發", "tag": "嵌入式系統開發類"},
    {"key": "DSE", "cate": "系統開發", "tag": "軟體工程類"}

]


def getcate(x):
    mongo.collection.update_many({"Class_ID": re.compile(x['key'])}, {'$set': {'cate': x['cate'], "tag": x['tag']}})


list(map(getcate, data))


# 養成班

# --- Class_name 課程名稱包含養成班
ProDev = mongo.collection.find({'Class_Name': re.compile('養成班')})
print("ProDev",ProDev.count())

for i in ProDev:
    # print(i)
    mongo.collection.update_one({"_id":i['_id']},{'$set': {'cate': "養成班", "tag": "養成班"}})


# 認證

# --- Class_name 課程名稱包含認證

certificate = mongo.collection.find({'Class_Name': re.compile('認證')})
print("certificate",certificate.count())

for i in certificate:
    # print(i)
    mongo.collection.update_one({"_id":i['_id']},{'$set': {'cate': "認證", "tag": "認證"}})


# 未分類
notag = mongo.collection.find({'tag': {'$exists': False}})
print(notag)

for i in notag:
    # print(i)
    mongo.collection.update_one({"_id":i['_id']},{'$set': {'cate': "未分類", "tag": "未分類"}})

# mongo.collection.update_one({"cate":i['_id']},{'$set': {'cate': "認證", "tag": "認證"}})