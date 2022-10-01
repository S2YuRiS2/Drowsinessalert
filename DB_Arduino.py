import time
import serial

import MySQLdb

port = serial.Serial("/dev/ttyACM0", baudrate=9600)

db = MySQLdb.connect("127.0.0.1", "root", "dbfldbqls12!", "sensor")
curs = db.cursor()

id = 1
while True:
    try:
        if port.in_waiting != 0:
            co2_value = port.readline()
            co2_value = (str)(co2_value[:-2].decode())

            heartbeat_value = port.readline()
            heartbeat_value = (str)(heartbeat_value[:-2].decode())

            print("id : " + str(id))
            print("co2_value : "+ str(co2_value))
            print("heartbeat_value : "+ str(heartbeat_value))

            curs.execute("""INSERT INTO info (id, co2_value, heartbeat_value) VALUES (%s, %s, %s)""",
                         (id, co2_value, heartbeat_value))

            db.commit()

            time.sleep(0.5)
            id += 1
    except KeyboardInterrupt:
        break
port.close()
db.close()
