
from myhelper import conf
from myhelper import MongoHelper

import re

mongo = MongoHelper(**conf.MongoDB_iiiedu)


langs = [
    {"lang": "Python", "in": ["python", "Python"]},
    {"lang": "C語言", "in": ["C語言"]},
    {"lang": "Java", "in": ["Java"]},
    {"lang": "C++", "in": ["C+\\+"]},
    {"lang": "C#", "in": ["C#"]},
    {"lang": "R", "in": ["R語言", "R軟體"]},
    {"lang": "JavaScript", "in": ["JavaScript"]},
    {"lang": "PHP", "in": ["PHP"]},
    {"lang": "Go", "in": ["Go語言"]},
    {"lang": "Swift", "in": ["Swift"]}
]


def get_in_langs(data):
    lang = data["lang"]
    inlist = data["in"]

    contains = [f["_id"] for f in mongo.collection.find(
        {
            'Class_Name': {"$in": [re.compile(i) for i in inlist]}
        }
    )]

    data = {'lang': lang, "contains_id": contains}

    return data


totals = list(map(get_in_langs, langs))
print(totals)


def add_db_field(data):
    lang = data["lang"]
    contains_id = data["contains_id"]

    mongo.collection.update_many({'_id': {'$in': contains_id}}, {'$set': {'lang': lang}})


# 分類
list(map(add_db_field, totals))
