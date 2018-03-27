# useMongoDBClass.py
# Author: Moises Marin
# Date: December 3, 2017
# Purpose: Define DB class
#
#

from mongodb import MongoConnect


mongo=MongoConnect("./_config/links-to-download")
pipe = [{ '$group' : { '_id': None, 'max': { '$max' : "$basePrice" }}}]
results=mongo.query_collection("trajes",pipe)
for doc in results:
    print doc
mongo.close_connection()
