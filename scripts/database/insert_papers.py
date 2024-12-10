import os
import json
from pymongo import MongoClient

def insert_json_to_mongodb(directory, db_name, collection_name, mongo_uri):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    collection.insert_one(data['abstracts-retrieval-response'])
                    print(f"Inserted {file} into {collection_name} collection")

if __name__ == "__main__":
    data_directory = './fix_file_ext_data'
    database_name = 'datasci'
    collection_name = 'papers'
    mongo_uri = 'mongodb://datasci:scopus888@localhost:27017'
    
    insert_json_to_mongodb(data_directory, database_name, collection_name, mongo_uri)