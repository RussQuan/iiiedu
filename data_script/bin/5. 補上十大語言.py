#!/usr/bin/python
# -*- coding: utf-8 -*-

from myhelper import conf,MongoHelper

from iiiedu import models

mongo = MongoHelper(**conf.MongoDB_iiiedu)

# iiidata = mongo.mongo_to_datalist({})


iiidata = mongo.collection.find({'lang': {'$exists': True}})


# print(list(iiidata))


def get_or_create(obj, **kwargs):
    data = dict(kwargs)
    try:
        t = obj.objects.get(**data)
        return t
    except:
        t = obj(**data)
        t.save()
        return t


def push_database(m):
    lang = get_or_create(models.Leng,name=m['lang'])
    course = get_or_create(models.Course,mongo_id=str(m['_id']))

    course.leng.add(lang)
    course.save()
    return [course.name,m['lang']]



p = list(map(push_database,iiidata))
print(p)