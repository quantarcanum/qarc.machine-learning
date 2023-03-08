import pandas as pd
from pandas import DataFrame
import json
from pymongo import MongoClient
from bson import json_util, ObjectId
from constants.constants import (
    MONGO_CONNECTION_STRING,
    MONGO_QUANTARCANUM_DB,
    MONGO_BAR_COLLECTION
)

class BarRepository():

    def __init__(self):
        self.client = self._get_database()
        self.collection = self._get_bar_collection()

    def _get_database(self):
        client = MongoClient(MONGO_CONNECTION_STRING)   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        return client[MONGO_QUANTARCANUM_DB]            # Return the database

    def _get_bar_collection(self):
        db = self._get_database()
        collection = db[MONGO_BAR_COLLECTION]
        return collection
    
    def get_bar_dataframe(self, normalized):
        jsonDocs = self.get_trbars_jsondocs()

        if normalized == True:
            return self._mongo_to_normalized_dataframe(jsonDocs)
        else:
            return self._mongo_to_dataframe(jsonDocs)
        
    def get_trbars_jsondocs(self):
            return self.collection.find()

    ####### UTILS ########
    def _mongo_to_normalized_dataframe(self, mongo_data):
        sanitized = json.loads(json_util.dumps(mongo_data))
        normalized = pd.json_normalize(sanitized)
        df = pd.DataFrame(normalized)
        return df

    def _mongo_to_dataframe(self, mongo_data):
        sanitized = json.loads(json_util.dumps(mongo_data))
        df = DataFrame(list(sanitized))
        df["Time"] = df["Time"].apply(lambda x: pd.to_datetime(x['$date']))
        df["LastTime"] = df["LastTime"].apply(lambda x: pd.to_datetime(x['$date']))
        return df