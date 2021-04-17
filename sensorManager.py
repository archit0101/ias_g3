from flask import Flask, jsonify, Response, request
import time
import requests
import json
import Dao as dao

from pykafka import KafkaClient
from pykafka.common import OffsetType
import json
dataBaseHelper = dao.DBHelper()


app = Flask(__name__)


@app.route('/registerNewSensorClass/<sensorDetails>')
def register_sensors(sensorDetails):
    y = eval(sensorDetails)
    #print("\n\n\nCHECKOUT SENSOR REGISTRATION", dataBaseHelper.registerNewSensorClass(y))
    #print(str(json.dumps(dataBaseHelper.registerNewSensorClass(y))))
    return str(json.dumps(dataBaseHelper.registerNewSensorClass(y)))


@app.route('/makeSensorInstances/<instanceDetails>')
def make_instances_of_sensors(instanceDetails):
    y = eval(instanceDetails)
    #print("\n\n\nCHECKOUT SENSOR INSTANCES", dataBaseHelper.makeSensorInstances(y))
    return dataBaseHelper.makeSensorInstances(y)


@app.route('/getSensorIdByLocation/<sensorLocation>')
def getSensorIdByLocation(sensorLocation):
    y = eval(sensorLocation)
    #print("\n\n\nCHECKOUT SENSOR BY LOCATION", dataBaseHelper.getSensorIdByLocation(y))
    return dataBaseHelper.getSensorIdByLocation(y)

@app.route('/sendNotification/<body>')
def sendNotification(body):
    dataBaseHelper.sendNotification(body)
    return "Sent"


@app.route('/validateAppSensors/<program_sensors>')
def validateAppSensors(program_sensors):
    y = eval(program_sensors)
    #print("\n\n\nCHECKOUT SENSOR BY LOCATION", dataBaseHelper.validateAppSensors(y))
    return dataBaseHelper.validateAppSensors(y)

def consume(sensorID,field):
    client = KafkaClient(hosts='localhost:9092')
    for i in client.topics[sensorID].get_simple_consumer(auto_offset_reset=OffsetType.LATEST,reset_offset_on_start=True):
        data_json = i.value.decode()
        data = json.loads(data_json)
        print(data)
        print(str(data[field]))
        return str(data[field])

@app.route('/getSensorData/<sensorID>/<field>')
def getSensorData(sensorID, field):
    print(sensorID, field)
    return consume(sensorID,field)


@app.route('/changeControllerState/<sensorID>/<field>/<newValue>')
def changeControllerState(sensorID, field, newValue):
    ipPort=dataBaseHelper.getIpPortOfSensor(sensorID)
    url="http://"+ipPort+"/set"+str(field)+"/"+str(newValue)
    print("url************************************88",url)
    response = requests.get(url)
    return "ok"


if __name__ == '__main__':
    app.run(port = 5000)
