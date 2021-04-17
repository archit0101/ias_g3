import pymongo
from pymongo import MongoClient
import json
import smtplib
cluster = MongoClient("mongodb+srv://SNSTeam:1234@mycluster.wrkyk.mongodb.net/IAS_Project?retryWrites=true&w=majority")

db = cluster["IAS_Project"]
sensor_class_collection = db["sensorClass"]
sensor_instance_collection = db["sensorInstance"]

# always have _db tag , it create bunch of dictionary associated with value
#post = {"_id": 1, "name": "lin", "score": 5}

#key is userId & value is Participant object
class DBHelper:
    def registerNewSensorClass(self,data):
        result=dict()
        success=""
        msg=""
        try:
            primaryKey={"_id":data.get("sensorClass")}
            # print(primaryKey)
            data.update(primaryKey)
            # print(data)
            try:
                sensor_class_collection.insert_one(data)
                success="True"
                msg="Sensor Class registered successfully!!!"
                self.sendNotification("New sensorclass registered on platform")
            except :
                success="False"
                msg="Sensor Class already present!!!!!"
                self.sendNotification("New sensorclass registered failed on platform")
        except:
            success="False"
            msg="Sensor Class field is missing!!!!"
            self.sendNotification("New sensorclass registered failed on platform")
        result["success_status"]=success
        result["msg"]=msg
        
        return str(result)
    

    def makeSensorInstances(self,data):
        data=data.get("instances")
        result=dict()
        allInstances=list()
        success=""
        msg=""
        for d in data:
            try:
                primaryKey={"_id":d.get("sensorId")}
                d.update(primaryKey)
                if self.checkIfsensorClassExists(d.get("sensorClass")):
                    try:
                        sensor_instance_collection.insert_one(d)
                        success="True"
                        msg="Sensor instance registered successfully!!!"
                        self.sendNotification("New sensor instance on platform")
                    except :
                        success="False"
                        msg="Sensor instance already present with ID: " + d.get("sensorId")
                        self.sendNotification("New sensor instance registration failed on platform")
                else:
                    success="False"
                    msg="Sensor class does not exists!!!!!!"
                    self.sendNotification("New sensor instance registration failed on platform")
            except:
                success="False"
                msg="Sensor Id field is missing!!!!"
                self.sendNotification("New sensor instance registration failed on platform")
            result["success_status"]=success
            result["msg"]=msg
            allInstances.append(result.copy())
        self.sendNotification(str(allInstances))
        return str(allInstances)

    def checkIfsensorClassExists(self, key):
        results = sensor_class_collection.find({"_id":key})
        for result in results:
            if (key==result["_id"]):
                return True
        return False

    
    def checkIfsensorClassAtLocationExists(self,sensorClass,location):
        results = sensor_instance_collection.find({"sensorClass":sensorClass, "location": location})
        for result in results:
            return result["sensorId"]
        return False

    
    def getSensorIdByLocation(self,data):
        data=data.get("requirement")
        #result=dict()
        allInstances=list()
        success=""
        msg=""
        for d in data:
            try:
                primaryKey={"_id":d.get("sensorClass")}
                d.update(primaryKey)
                ID = self.checkIfsensorClassAtLocationExists(d.get("sensorClass"), d.get("location"))
                if ID:
                    #success="True"
                    msg = ID
                else:
                    return str("False")
                    #msg="Sensor instance at location absent!!!"
            except:
                # success="False"
                # msg="Requirement field is missing!!!!"
                return str("False")
            # result["success_status"]=success
            # result["msg"]=msg
            allInstances.append(msg) 
        return str(allInstances)

    def validateAppSensors(self,data):
        data=data.get("classes")
        result=list()
        for d in data:
            result.append(self.checkIfsensorClassExists(d))
        return str(result)

    def getIpPortOfSensor(self,sensorId):
        results = sensor_instance_collection.find({"sensorId":sensorId})
        for result in results:
            return result["ip"]+":"+result["port"]
        return False

    def sendNotification(self,body):
        
        sender='wtrending17@gmail.com'
        receiver='somyalalwani9@gmail.com'
        password='Kunal@iiit'
        smtpserver=smtplib.SMTP("smtp.gmail.com",587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(sender,password)
        print("****************************")
        print("receiver: ",receiver)
        print(body)
        print("*************************")
        msg='Subject:An activity occured on the platform\n'+str(body)
        smtpserver.sendmail(sender,receiver,msg)
        print('Sent notification')
        smtpserver.close()







db=DBHelper()
# with open('assets/sensorDetails.json') as f:
#     data = json.load(f)
#     print(data)
#     print(type(data), "check type")
#     print(db.registerNewSensorClass(data))

# with open('assets/sensorInstance.json') as f:
#     data = json.load(f)
#     print(data)
#     print(type(data), "check type")
#     print(db.makeSensorInstances(data))

# with open('assets/userRequirement.json') as f:
# data = json.load(f)
# # print(data)
# print(db.getSensorIdByLocation(data))

# print(db.checkIfKeyExists("shaitan_temp5"))
# print(db.getIpPortOfSensor("S115"))