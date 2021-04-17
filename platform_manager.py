import socket
import _thread
import SensorManager as sm
#import sensorRPC as sm
import shutil
import json
import ast
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5001     # The port used by the server


def thread_conn(s,py_file_data,clientfd): #with scheduler
    HOST='127.0.0.1'
    PORT=8081
    with socket.socket (socket.AF_INET, socket.SOCK_STREAM) as clientsocket:
        clientsocket.connect((HOST, PORT)) 
        clientsocket.sendall(str(s).encode())
        print("####################")
        print(s)
        print("####################")
        ans=clientsocket.recv(1024).decode()
        if ans=="RECEIVED":
            clientsocket.sendall(str(py_file_data).encode())
            print(py_file_data)
            ans=clientsocket.recv(1024).decode()
        else:
            clientsocket.sendall(str("recvd error msg").encode())
            ans=clientsocket.recv(1024).decode()
    clientfd.sendall(str(ans).encode())




def start_server(clientfd):
    while(1):
        query=clientfd.recv(5000).decode()
        #print(app_name)
        tokens=query.split("*")
        if tokens[0] == "app":
            if tokens[1]== "admin":
                print(1)

                #class installation
                if tokens[2] == "1":
                    print(3)
                    data=tokens[3]
                    #response=str(sm.registerNewSensorClass(data).text)
                    response=str(sm.registerNewSensorClass(data))
                    print(response)
                    clientfd.sendall(response.encode())
                
                # instance installation
                if tokens[2] == "2":
                    print(4)
                    data=tokens[3]
                    #response=str(sm.makeSensorInstances(data).text)
                    response=str(sm.makeSensorInstances(data))
                    print(response)
                    clientfd.sendall(response.encode())


                
                # upload application
                if tokens[2] == "3":
                    print(5)
                    data = tokens[3]
                    #response=str(sm.validateAppSensors(data).text)
                    response=str(sm.validateAppSensors(data))
                    print(response)
                    clientfd.sendall(response.encode())
            
            
            if tokens[1] == "user":
                print(2)
                #t=json.dumps(lst[i])
                #data1 = json.dumps(tokens[2]) #kunal wali file
                print(tokens[3])
                response=tokens[3]
                r=response.replace("'",'"')
                data2 = json.loads(r)  #for archi
                selected_app=tokens[4]
                print(data2, type (data2))
                sid=dict()
                #sid = sm.getSensorIdByLocation(tokens[2]).text #kunal wala
                lst = sm.getSensorIdByLocation(tokens[2])
                s=""
                s+=str(data2["starttime"])
                s+="*"
                s+=str(data2["endtime"])
                s+="*"
                s+=str(data2["recurring_bit"])
                s+="*"
                s+=str(data2["recurring_interval"])
                s+="*"
                s+=selected_app
                s+="*"
                s+=(str(lst))
                #sid["starttime"]=data2["starttime"]
                '''
                sid["endtime"]=data2["endtime"]
                sid["recurring_bit"]=data2["recurring_bit"]
                sid["recurring_interval"]=data2["recurring_interval"]
                sid["appname"]=selected_app
                sid["sid"]=lst
                '''
                _thread.start_new_thread(thread_conn, (s,tokens[3],clientfd)) 

        



def server():
    serverfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #comSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverfd.bind((HOST,PORT))
    serverfd.listen(5)
    print("*****************************")
    print("Server Established")
    print("*****************************")
    while(1):
        clientfd,add=serverfd.accept()
        _thread.start_new_thread(start_server,(clientfd,))
        #start_new_thread(start_server, (clientfd,))
    serverfd.close()


server()