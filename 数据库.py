import pymysql
import time
import datetime


con =  pymysql.connect(
    host = '127.0.0.1',
    user = 'root',
    passwd = 'Knight1205',
    db = 'car_user',
    charset = 'utf8'
)
cur = con.cursor()

car_number = '豫A210M0'
position = 'A123'


now = datetime.datetime.now()
cur.executemany("INSERT INTO Car(CarNumber,Position,InTime) VALUES(%s,%s,%s)",[(car_number,position,now.strftime("%Y-%m-%d %H:%M:%S"))])
con.commit()