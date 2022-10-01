import pymysql
import time

mysqldb = pymysql.connect(
    user = 'root',
    passwd= 'dbfldbqls12!',
    host = '127.0.0.1',
    db = 'sensor',
    charset = 'utf8'
)

cursor = mysqldb.cursor()
sql = "select co2_value, heartbeat_value from sensor"

cursor.execute(sql)
mysqldb.commit()
datas = cursor.fetchone()

# print(datas)
while datas:
    co2_value = datas[0]
    heartbeat_value = datas[1]
    print(co2_value)
    print(heartbeat_value)

    time.sleep(2)



