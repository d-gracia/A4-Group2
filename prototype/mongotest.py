from pymongo import MongoClient
from pymongo.server_api import ServerApi
 
#client = pymongo.MongoClient("mongodb+srv://\
#                            <username>:<password>\
#                            @cluster0.2tsfg.mongodb.net/cluster0-shard-00-02.2tsfg.mongodb.net:27017retryWrites=true&w=majority", server_api=ServerApi('1'))
#db = client.test


#client = pymongo.MongoClient("https://us-east-1.aws.data.mongodb-api.com/app/a4-group2-mlhgj/endpoint/test_endpoint", server_api=ServerApi('1'))
#db = client.test

from pymongo import MongoClient
uri = "mongodb+srv://cluster0.2tsfg.mongodb.net/api_key_test?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='/Users/finheadley/cs_411_app/flaskmongotest/admin_user.pem',
                     server_api=ServerApi('1'))
db = client['api_key_test']
collection = db['key']



#doc_count = collection.count_documents({})
#print(doc_count)

#myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#mydb = myclient["mydatabase"]
#mycol = mydb["customers"]

#mydict = { "dogs": "back", "fish": "baaaaa" }

#x = collection.insert_one(mydict)

# collection.insert_one(
#    {
#      "_id": 100,
#      "quantity": 250,
#      "instock": "true",
#      "reorder": "false",
#      "details": { "model": "14QQ", "make": "Clothes Corp" },
#      "tags": [ "apparel", "clothing" ],
#      "ratings": [ { "by": "Customer007", "rating": 4 } ]
#    }
# )
print(collection.find_one({ "_id": 100 }))
# collection.update_one(
#    { "_id": 100 },
#    { "$set":
#       {
#         "quantity": 500,
#         "details": { "model": "2600", "make": "Fashionaires" },
#         "tags": [ "coats", "outerwear", "clothing" ]
#       }
#    }
# )





"""
serverStatusResult=db.command("serverStatus")
#print("doc Count:",doc_count)
print()
print("status:",serverStatusResult)

"""
