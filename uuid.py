import sqlite3
import json
import Levenshtein

#データベース接続
db = "db.sqlite3"
connection = sqlite3.connect(db)
cur = connection.cursor()

def database(sql):
    cur.execute(sql)
    return cur.fetchall()

sql_all = 'SELECT device_uuid FROM fingerprint_fingerprint'

uuid_list = []

data = database(sql_all)
for i in range (len(data)):
    uuid = (data[i])[0]
    if uuid not in uuid_list:
        uuid_list.append(uuid)
print(len(uuid_list))
print(uuid_list)



#データベース接続終わり
cur.close()
connection.close()
