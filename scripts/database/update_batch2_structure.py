from pymongo import MongoClient

client = MongoClient("mongodb://datasci:scopus888@datascidb.kanakornmek.dev:27017/?authSource=admin")

db = client['datasci']
collection = db['papers']

collection.update_many(
    { "batches": 2, "subject-areas.subject-area": { "$exists": True, "$type": "array" } },
    [
        {
            "$set": {
                "subject-areas.subject-area": {
                    "$map": {
                        "input": "$subject-areas.subject-area",
                        "as": "item",
                        "in": { "@abbrev": "$$item" }
                    }
                }
            }
        }
    ]
)
