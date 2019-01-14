from pymongo import MongoClient
import pandas as pd


class MongoHelper(object):
    def __init__(self, host, db_name, collection):
        client = MongoClient(host)
        db = client[db_name]
        self.collection = db[collection]

    def mongo_to_dataframe(self, query={}, no_id=None):
        cursor = self.collection.find(query)
        df = pd.DataFrame(list(cursor))
        if no_id:
            del df['_id']

        return df

    def dataframe_to_mongo(self, df):
        self.collection.insert_many(df.to_dict('records'))

    def mongo_to_datalist(self, query):
        cursor = self.collection.find(query)

        df = list(cursor)
        return df

    def mongo_aggregate_datalist(self, query):
        cursor = self.collection.aggregate(query)

        df = list(cursor)
        return df