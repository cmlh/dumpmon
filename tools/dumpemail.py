from pymongo import MongoClient
from settings import USE_DB, DB_HOST, DB_PORT

client = MongoClient(DB_HOST, DB_PORT).paste_db.pastes

def uniqueEmailSet():
        map = Code("function () {"
                   " this.emails.forEach(function(z) {"
                   "    emit(z,1);"
                   "    });"
                   "}")
        reduce = Code("function (key,values) {"
                      "var total = 0;"
                      "for (var i = 0; i <values.length; i++) {"
                      "    total += values[i];"
                      "}"
                      "return total;"
                    "}")
        result = client.map_reduce(map,reduce,"res") 
        return result 

uniqueEmailSet()