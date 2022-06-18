"""
OfflineLog.py

Description: Offline log system for the AIO system.

@__Author --> Created by Jeppe Mikkelsen aka JepMik
@__Date & Time --> Created on 18/06/2022
@__Email --> = Jepmik@live.dk
@__Version --> = 1.0
@__Status --> = Dev
"""
#JSON translator for offline log
#from Client import Client
#from Network import Network
from cmath import log
import json



props = {
    'temperature': 1,
    'concentration': 23,
    'systemActive': True,
    'wifiConnection': False,
    'aioConnection': False,
    'offlineAgain': True #If the system is offline again, it will append to the log file again else overwrite the log file
}

#write Properties to the log file in string format
def OfflineLog(props):
    #Create the log file
    if (props['offlineAgain']): 
        with open('OfflineLogT.txt', 'a') as logFile:
            logFile.write("temperature:" +"^" + str(props['temperature']))
            logFile.write('\n')
            logFile.write("concentration:" +"^" + str(props['concentration']))
            logFile.write('\n')
            logFile.close()
    else: #Create a new log file
        with open('OfflineLogT.txt', 'w') as logFile:
            logFile.write("temperature:" + "^" + str(props['temperature']))
            logFile.write('\n')
            logFile.write("concentration:" + "^" + str(props['concentration']))
            logFile.close()

for i in range(2):
    OfflineLog(props)

#Read the txt log and generate complete JSON
def jsonFile():
    Log = open('OfflineLogT.txt')
    list = Log.readlines()
    data = []
    #values = []
    
    pubAmount = len(list)
    for line in list:
        line.replace('\n', '')
        key, value = line.split('^')
        data.append({key: value},)
    
    #result = {"results": [values]}
    #jsondumps converts the data to JSON
    jsonData = json.dumps(data, indent=4)
    return jsonData, pubAmount
    

jsonData, pubAmount = jsonFile()



#LogFile creation to run while system is offline
def OfflineLog(jsonData):
    with open('OfflineLog.json', 'w') as logFile:
        logFile.write(jsonData)
        logFile.close()

for i in range(pubAmount):
    OfflineLog()




#Reading log file and publishing to AIO
print("Reading log file...")
def readJSON():
    #Read the log file
    f = open('OfflineLog.json')
    
    
    for line in f:
        data = json.loads(line)
        print(data)
        
        #if key == 'temperature':
           # print("Publishing temperature...")
            #client.publish(makeFeedname('temperature'),bytes(value,'utf-8'),qos=0)
       # elif key == 'concentration':
      #      print("Publishing concentration...")
            #client.publish(makeFeedname('concentration'),bytes(value,'utf-8'),qos=0)
readJSON()
    


