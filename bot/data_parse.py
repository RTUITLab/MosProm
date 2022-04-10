import asyncio
import json
import math
import secrets
import threading
import time
import csv

import numpy as np
import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from fastapi.responses import FileResponse
import socketio
import random
import telebot
import threading
import numpy as np
import matplotlib.pyplot as plt
bot = telebot.TeleBot("1944967971:AAEjIywx-faIMC7m8UvqYrIQ2Ih6Hb-EFmI")
data_user = {}

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*'
)
sio_app = socketio.ASGIApp(sio)




app = FastAPI()
app.mount('/case/2/ws', sio_app)

data_case = {}
qr_que = []
qr_secret = secrets.token_urlsafe(10)
qr_que.append(qr_secret)

data_json = {
    "axelerometr":{
        "x":0.0,
        "y":0.0,
        "z":9.8
    },
    "stopsAmount": 0,
    "mileage": 0.0
}

@sio.event
async def connect(sid, environ, auth=None):
    print(f"{sid} is connected.")
    print(auth)
    sio.save_session(sid, {"authorized": True})
    # if 'token' in auth and auth['token'] in qr_que:
    #     await sio.save_session(sid, {"authorized": True})
    #     for i in data_case:
    #         data = {"topic": i, "msg": data_case[i]}
    #         print("data _______", data)
    #         await sio.emit('topic_data', data)
    # elif "qr_viewer_key" in auth and auth["qr_viewer_key"] == "#qwe":
    #     await sio.save_session(sid, {"authorized": False})
    #     await sio.emit('new_qr', {"qr_secret": qr_secret}, sid)
    # else:
    #
    #     raise ConnectionRefusedError('authentication failed')


@sio.on('button')
async def setState(sid, data: object):
    session = await sio.get_session(sid)
    # if not session["authorized"]:
    #     return
    print(f'sender-{sid}: ', data)

@sio.on('send_alert')
async def sendAlert(sid, data: object):
    bot.send_message(chat_id=835777342,text="Значение "+"превысило")

@app.get("/get_data")
def getAxl():
    with open('go_false_true.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            print(row)

@app.get("/img")
async def getImg():
    return FileResponse("saved_figure.png")

def calc_pred(x,y1):
    t = int(y1[0])
    x1 = np.array(y1)
    y = np.array(x)
    mx = x1.sum() / len(x1)
    my = y.sum() / len(y)
    a2 = np.dot(x1.T, x1) / len(x1)
    a11 = np.dot(x1.T, y) / len(y)

    kk = (a11 - mx * my) / (a2 - mx ** 2)
    bb = my - kk * mx

    ff = [kk * z + bb for z in range(t,t+len(y1) + 100)]

    return [ff, [z for z in range(t,t+len(y1) + 100)]]

def max_value(sss,y):
    server = "http://192.168.137.207:8000"

    return [18.3 for z in range(len(y))]

async def generate_data():
    revolutions = []
    humidity = []
    vibration = []
    x1 = []
    x2 = []
    x3 = []
    x4 = []
    x5 = []
    y = []
    with open('predictive-maintenance-dataset.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for index, row in enumerate(spamreader):
            if index > 0:
                revolutions.append(float(row[1]))
                humidity.append(float(row[2]))
                vibration.append(float(row[3]))
                x1.append(float(row[4]))
                x2.append(float(row[5]))
                x3.append(float(row[6]))
                x4.append(float(row[7]))
                x5.append(float(row[8]))
                y.append(float(row[0]))
                if len(y) > 200:
                    revolutions.pop(0)
                    humidity.pop(0)
                    vibration.pop(0)
                    x1.pop(0)
                    x2.pop(0)
                    x3.pop(0)
                    x4.pop(0)
                    x5.pop(0)
                    y.pop(0)
                # print(revolutions,y)
                if len(y)>2:
                    await sio.emit("change_color", {"revolutions":{'x':revolutions,'y':y, 'pred_x':calc_pred(revolutions,y)[0],'pred_y':calc_pred(revolutions,y)[1], "max_x":max_value("revolutions",y),"max_y":y},
                                                    "humidity":{'x':humidity,'y':y, 'pred_x':calc_pred(humidity,y)[0],'pred_y':calc_pred(humidity,y)[1], "max_x":max_value("humidity",y),"max_y":y},
                                                    "vibration":{'x':vibration,'y':y, 'pred_x':calc_pred(vibration,y)[0],'pred_y':calc_pred(vibration,y)[1], "max_x":max_value("vibration",y),"max_y":y},
                                                    "x1":{'x':x1,'y':y, 'pred_x':calc_pred(x1,y)[0],'pred_y':calc_pred(x1,y)[1], "max_x":max_value("x1",y),"max_y":y},
                                                    "x2":{'x':x2,'y':y, 'pred_x':calc_pred(x2,y)[0],'pred_y':calc_pred(x2,y)[1], "max_x":max_value("x2",y),"max_y":y},
                                                    "x3":{'x':x3,'y':y, 'pred_x':calc_pred(x3,y)[0],'pred_y':calc_pred(x3,y)[1], "max_x":max_value("x3",y),"max_y":y},
                                                    "x4":{'x':x4,'y':y, 'pred_x':calc_pred(x4,y)[0],'pred_y':calc_pred(x4,y)[1], "max_x":max_value("x4",y),"max_y":y},
                                                    "x5":{'x':x5,'y':y, 'pred_x':calc_pred(x5,y)[0],'pred_y':calc_pred(x5,y)[1], "max_x":max_value("x5",y),"max_y":y},
                                                    })


            time.sleep(2)

    return {'x1':x1,'y':y}

threading.Thread(target=asyncio.run,args=(generate_data(),)).start()