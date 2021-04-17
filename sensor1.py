import threading
import time
import random
from _thread import *
import json
import requests
from flask import Flask, jsonify, Response, request
from pykafka import KafkaClient
import sys

app = Flask(__name__)

##### INPUT FORMAT python3 sensor1.py sensorID port

currentTemp=0
ACState="off"
ACTemp=40

@app.route('/getCurrentTemp')
def getCurrentTemp():
    global currentTemp
    global ACTemp
    currentTemp=random.randint(40,45)
    if ACState.lower()=="on" :
        currentTemp=int(currentTemp)+int(ACTemp)-40
    return str(currentTemp)

def getACState():
    return str(ACState)

def getACTemp():
    return ACTemp

@app.route('/setACState/<val>')
def setACState(val):
    global ACState
    ACState=val
    return "ok"

@app.route('/setACTemp/<val>')
def setACTemp(val):
    global ACTemp
    ACTemp=val
    return "ok"


def kafkaStream():
    topicName = sys.argv[1]
    
    client = KafkaClient(hosts='localhost:9092')
    topic = client.topics[topicName]
    producer = topic.get_sync_producer()
    i = 0
    while True:
        currTemp = getCurrentTemp()
        ACState = getACState()
        ACTemp = getACTemp()

        dict = {'currentTemp' : currTemp, 'ACState' : ACState, 'ACTemp' : ACTemp}
        dict_json = json.dumps(dict)

        producer.produce(dict_json.encode())
        print(dict_json)
        time.sleep(5)

t=threading.Thread(target=kafkaStream,name="t")
t.start()

if __name__ == '__main__':
    app.run(port = int(sys.argv[2]))

    
