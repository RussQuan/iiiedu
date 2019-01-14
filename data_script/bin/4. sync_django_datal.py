#!/usr/bin/python
# -*- coding: utf-8 -*-


from myhelper import MongoHelper,conf

from iiiedu import models

mongo = MongoHelper(**conf.MongoDB_iiiedu)

iiidata = mongo.mongo_to_datalist({})

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
    # Cate表
    cate = get_or_create(models.Cate, name=str(m["cate"]))
    print("cate", cate.id)

    # Tag表

    tag = models.Tag.objects.filter(**{'name': str(m['tag'])})
    if len(tag) == 0:
        data = {'name': m['tag'], 'cate': cate}
        tag = models.Tag(**data)
        tag.save()
    else:
        tag = tag[0]
    print('tag', tag.id)

    # Branch 表

    branch = models.Branch.objects.filter(**{'md5_address': m["md5_address"]})
    if len(branch) == 0:
        branch = models.Branch(
            **{'unit': m["unit"], "city": m["city"], "addr": m["address"], "md5_address": m["md5_address"]})
        branch.save()
    else:
        branch = branch[0]
    print("branch", branch.id)

    # Lang 表


    # Course 表
    courseData = {
        "class_id": m["Class_ID"],
        "mongo_id": str(m["_id"]),

        "name": m["Class_Name"],
        "summary": m["Course_content"],
        "Price_Ownpay": m["Price_Ownpay"],
        "Training_EndDate": m["Training_EndDate"],
        "Training_Hours": m["Training_Hours"],
        "Training_StartDate": m["Training_StartDate"],
        "link": m["link"],

        "Tag": tag,
        "branch": branch,

    }
    course = models.Course.objects.filter(**{'mongo_id': str(m["_id"])})
    if len(course) == 0:
        course = models.Course(**courseData)
        course.save()
    else:
        course = course[0]
    return course.name



p = list(map(push_database,iiidata))
print(p)
