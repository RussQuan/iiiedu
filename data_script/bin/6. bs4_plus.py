
from myhelper import MongoHelper,bs4_crawl,conf
from iiiedu.models import Course, Theme, Series


mongo = MongoHelper(**conf.MongoDB_iiiedu)
iiiedu_temp = MongoHelper(**conf.MongoDB_Temp)



def foo(data):
    if "售前規劃顧問(Pre-sales)培訓班" in data['name']:
        data['name'] = "售前規劃顧問(Pre-Sales)培訓班"
    x = mongo.collection.find({'Class_Name': data['name']}, {'_id': 0, 'Class_Name': 1, 'Training_StartDate': 1})
    # print(list(x))

    find_name = []
    for i in x:
        # print(i['Class_Name'])
        iiiedu_temp.collection.insert_one({
            'Class_Name': i['Class_Name'],
            'series': data['series'],
            'theme': data['theme'],
            'Training_StartDate': i['Training_StartDate']

        })
        find_name.append(i['Class_Name'])

    ret = {"name": data['name'], "find": find_name}
    return ret


def bs4_mongo(data):

    iiiedu_temp.collection.drop()
    ret = list(map(foo, data))
    print(ret)


def get_or_create(obj, **kwargs):
    data = dict(kwargs)
    try:
        t = obj.objects.get(**data)
        return t
    except:
        t = obj(**data)
        t.save()
        return t


def insert_theme_series(data):
    theme_dict = {
        '大數據 / AI': 'ai',
        '資訊系統開發': "isd",
        '軟實力': "sw",
        '科技創新管理': "tim",
        '數位行銷': "dm",
        '資訊架構規劃': "iap",
        '智慧產業': "wi"
    }

    series_dict = {
        '管理能力': "ma",  # Management ability
        '大數據分析': "bda",  # Big data analysis
        '軟體架構\r\n\t\t\t與開發': "sad",  # Software Architecture and Development
        '專案管理': "pm",  # Project management
        '大數據處理': "bdp",  # Big data processing
        '簡報談判': "bn",  # Briefing negotiations
        'AI技術': "ait",  # AI technology
        'IT服務管理': "itsm",  # IT service management
        'AI應用': "aip",  # AI application
        '智慧綠能': "sge",  # Smart Green Energy
        '大數據應用': "bdapp",  # Big data application
        '物聯網': "iot",  # internet of thing
        '雲端運算': "cc",  # Cloud Computing
        '移動互聯網': 'mi',  # Mobile Internet
        '業務開發': 'bd',  # Business Development
        '智慧製造': 'sm',  # Smart manufacturing
        '金融科技': 'ft',  # Financial Technology
        '資訊安全': 'is',  # Information security
        '研發管理': 'rd',  # R&D management
        '創新設計': 'cd',  # Creative design
        '人資管理': 'hr',  # Human resources management
        '職場能力': 'wc',  # Workplace competence
    }


    theme = data['theme']
    t = get_or_create(Theme, name=theme)
    t.en = theme_dict[theme]
    t.save()

    series = data['series']
    s = get_or_create(Series, name=series)
    s.theme.add(t)
    s.en = series_dict[series]
    s.save()

    c = Course.objects.filter(name=data['name'])


    for i in c:
        i.series.add(s)
        print(i.name)
        return i.name


if __name__ == '__main__':


    data = bs4_crawl.main()

    # insent MongoDB
    bs4_mongo(data)

    # insent Mysql
    ret = list(map(insert_theme_series, data))
    print(ret)




