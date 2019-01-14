

from myhelper import MongoHelper
from myhelper import conf

import hashlib


mongo = MongoHelper(**conf.MongoDB_iiiedu)

def md5Encode(str):
    #参数必须是byte类型，否则报Unicode-objects must be encoded before hashing错误
    m = hashlib.md5(str.encode(encoding='utf-8'))
    return m.hexdigest()

x = mongo.collection.find()

for i in x:
    print(i["unit"]+i["city"]+i["address"])
    m = md5Encode(i["unit"]+i["city"]+i["address"])
    print(m)
    mongo.collection.update_one({"_id":i["_id"]},{"$set":{"md5_address":m}})

