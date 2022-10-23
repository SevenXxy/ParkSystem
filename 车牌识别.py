# encoding:utf-8

import json
import cv2 as cv
import requests
import base64
import datetime
import time
import pymysql 

#数据库连接信息
con =  pymysql.connect(
    host = '127.0.0.1',
    user = 'root',
    passwd = 'Knight1205',
    db = 'car_user',
    charset = 'utf8'
)
cur = con.cursor()





'''
获取token
# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=8Dn0PnT519Ob0GtrgyoacVch&client_secret=qeG2puL6TM2CO7iGhSqclDqiyBkiLBAG'
token = requests.get(host)
if token:
    print(token.json())
'''


'''
车牌识别
'''

#request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/license_plate"

#开启摄像头
cap = cv.VideoCapture(0)

#从摄像头获取图片
def img_get():
    f,frame = cap.read()
    cv.imwrite('car.jpg',frame)


# 二进制方式打开图片文件
def open_img():
    f = open('./car.jpg', 'rb')
    img = base64.b64encode(f.read())
    return img

#调用百度ai识别车牌
def recognize():
    params = {"image":img}
    access_token = '24.d03d97c15a1ac580ce1d0ce6ed97092e.2592000.1669085734.282335-26257050'
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/license_plate" + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        json_dict = response.json()
        words_result = json_dict['words_result']
        return (words_result['number'])

#给车辆分配的车位，此处暂时瞎编
position = 'A123'

if __name__ == '__main__':
    #一直循环执行，每60秒执行一次
    while(1):
        img_get()
        img = open_img()
        car_number = recognize()
        now = datetime.datetime.now()
        cur.executemany("INSERT INTO Car(CarNumber,Position,InTime) VALUES(%s,%s,%s)",[(car_number,position,now.strftime("%Y-%m-%d %H:%M:%S"))])
        con.commit()
        print(car_number)
        time.sleep(60)
