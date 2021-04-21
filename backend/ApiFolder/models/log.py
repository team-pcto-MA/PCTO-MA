import sqlite3 as sq
from . import DbSensors
def resToDict(res, field_names):

    res_list = []
    if(len(res) != 0 or res != None):
        for tupla in res: #tupla -> number of elements x tupla, every tupla has 6 values
            count = 0
            res_dict = {} #last tupla
            for field in field_names: #number of fields
                res_dict[f'{field}'] = tupla[count] #matching fields to corresponding res
                count += 1 #moving to the next value of the corresponding tupla, 1 - 2 - 3 - 4 - 5 - 6
            res_list.append(res_dict) #final dict of res, tupla "number" -> corresponding dict of values
        return res_list
    else:
        return None

class DbLog:
    def __init__(self):
        self.conn = sq.connect('MA_002.db')
        self.table = 'Log'

    
    def numberOfLogs(self,deviceID):
        try:
            
            cursore = self.conn.cursor()
            cursore.execute(f"SELECT count(*) FROM {self.table} WHERE deviceID == '{deviceID}'")
            num = cursore.fetchone()
            return num[0]
            
        except sq.Error as e:
            print(f" num logs Error -> {e}")

    def sensorLogs(self,deviceID):
        try:
            if(DbSensors.exist(self,deviceID)):
                cursore = self.conn.cursor()
                cursore.execute(f"SELECT E.event, L.whenEvent FROM {self.table} L, Events E WHERE L.event == E.id AND deviceID == '{deviceID}' ORDER BY whenEvent DESC")
                return resToDict(cursore.fetchall() , [i[0] for i in cursore.description])
            else:
                return "Invalid deviceID"
        except sq.Error as e:
            print(f"2 Error -> {e}")
    
    def lastLogs(self,mac):
        try:
            cursore = self.conn.cursor()
            cursore.execute(f"SELECT deviceID,event,whenEvent FROM {self.table},Sensors WHERE Sensors.dev_id = {self.table}.deviceID AND Sensors.mac_RSPi == '{mac}' GROUP BY deviceID HAVING max(idLog)")
            return resToDict(cursore.fetchall() , [i[0] for i in cursore.description]) 
        except sq.Error as e:
            print(f"3 Error -> {e}")
    
    def allLogsMac(self,mac): #logs order by deviceID and date
        try:
            cursore = self.conn.cursor()
            print(f"SELECT L.* FROM {self.table} L, Sensors S WHERE L.deviceID == S.dev_id AND S.mac_RSPi == '{mac}'")
            cursore.execute(f"SELECT L.*, E.event FROM {self.table} L, Sensors S , Events E WHERE L.deviceID == S.dev_id AND L.event == E.id AND S.mac_RSPi == '{mac}'")
            logs = cursore.fetchall()

            res, name_list = logs, [i[0] for i in cursore.description]
            return resToDict(res,name_list)
        except sq.Error as e:
            print(f"4 Error -> {e}")

    def allLogs(self): #logs order by deviceID and date
        try:
            cursore = self.conn.cursor()
            print(f"SELECT * FROM {self.table}")
            cursore.execute(f"SELECT * FROM {self.table}")
            logs = cursore.fetchall()

            res, name_list = logs, [i[0] for i in cursore.description]
            return resToDict(res,name_list)
        except sq.Error as e:
            print(f"4 Error -> {e}")

    def deleteAllLogsMac(self,mac): #logs order by deviceID and date
        try:
            cursore = self.conn.cursor()
            print(f"DELETE FROM {self.table} WHERE deviceID IN (SELECT L.deviceID FROM {self.table} L, Sensors S WHERE L.deviceID == S.dev_id AND S.mac_RSPi == '{mac}' )")
            cursore.execute(f"DELETE FROM {self.table} WHERE deviceID IN (SELECT L.deviceID FROM {self.table} L, Sensors S WHERE L.deviceID == S.dev_id AND S.mac_RSPi == '{mac}' )")
            self.conn.commit()
        except sq.Error as e:
            print(f"4 Error -> {e}")

    def InsertLog(self,deviceID,event,whenEvent):
        try:
            cursore = self.conn.cursor()

            logs = self.numberOfLogs(deviceID)
            print(logs)
            if(logs >= 25): 
                cursore.execute(f"DELETE FROM {self.table} WHERE deviceID == '{deviceID}' ORDER BY idLog LIMIT 1")
            print(f"QUERY :\nINSERT INTO {self.table} (deviceID,event,whenEvent) VALUES ('{deviceID}','{event}','{str(whenEvent)}')")
            cursore.execute(f"INSERT INTO {self.table} (deviceID,event,whenEvent) VALUES ('{deviceID}','{event}','{whenEvent}')")
            self.conn.commit()
            return True
        except sq.Error as e:
            print(f"inser Error -> {e}")
            return False

    def destroy(self):
        self.conn.close()