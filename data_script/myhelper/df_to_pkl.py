from myhelper.mongohelper import MongoHelper
from myhelper import conf

def export_pkl(conf_db,filename):

    mongo = MongoHelper(**conf_db)

    dfiii = mongo.mongo_to_dataframe({})

    dfiii = dfiii.drop('_id', axis=1)

    # 增加月份標記
    dfiii["Training_StartM"] = dfiii.Training_StartDate.dt.to_period('M')

    # 只篩選2018年的資料
    dfiii2018 = dfiii.set_index("Training_StartDate")["2018"].reset_index()


    dfiii2018.to_pickle(filename)



