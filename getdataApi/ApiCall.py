import requests
from pymongo import MongoClient

def insert_to_mongo(db_name, collection, mongo_uri, response):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection]
    data_new = []
    headers = {
        "X-ELS-APIKey": "faa5274eb341aee1f3c7877160d899de",  # Replace with your token
        "X-ELS-Insttoken": "2a99851e7ea868948a570d488a0ab64b",
        "Accept": "application/json"
    }
    response_json = response.json()
    for i in response_json["search-results"]["entry"]:
        for data in i['link']:
            if data['@ref'] == 'self':
                link = data['@href']
                break
        response_new = requests.get(link, headers=headers)
        response_json1 = response_new.json()
        try:
            response1 = response_json1['abstracts-retrieval-response']
        except KeyError:
            print(response_json1.keys())
            continue
        response1['batches'] = 1
        data_new.append(response1)
    try:
        collection.insert_many(data_new, ordered = False)
    except Exception as e:
        pass
    


# Define the API endpoint
url = "https://api.elsevier.com/content/search/scopus"  # Replace with the actual API endpoint

headers = {
    "X-ELS-APIKey": "faa5274eb341aee1f3c7877160d899de",  # Replace with your token
    "X-ELS-Insttoken": "2a99851e7ea868948a570d488a0ab64b"
}

params = {
    'httpAccept': ['application/json'],
    #'view': ['COMPLETE'],
    'date': ['2018-2023'],
    'query': ['SUBJAREA(EART)'],
    'cursor': '*',
    'count': ['200']
}
print(params['query'])
# Send the GET request
response = requests.get(url, params = params, headers = headers)
#print requests info
# print(response.headers)

uri = "mongodb://datasci:scopus888@datascidb.kanakornmek.dev:27017/?authSource=admin"
# Check if the request was successful
if response.status_code == 200:
    # Print the JSON response (if the response is in JSON format)
    insert_to_mongo("datasci", "papers", uri, response=response)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")




for i in range(4):
    response_json2 = response.json()
    params['cursor'] = response_json2['search-results']["cursor"]["@next"]
    response = requests.get(url, params = params, headers = headers)
    if response.status_code == 200:
        print(f"Cycle {i+1}")
        # Print the JSON response (if the response is in JSON format)
        insert_to_mongo("datasci", "papers", uri, response=response)
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code} cycle {i}")
print("--------------------------------")


