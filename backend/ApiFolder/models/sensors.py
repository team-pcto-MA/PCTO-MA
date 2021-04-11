import sqlite3 as sq
import datetime


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

class DbSensors:

    def __init__(self):
        self.conn = sq.connect('MA_002.db')
        self.table = 'Sensors'

    def addSensor(self , mac, id, t_id,f_v):
        try:

            cursore = self.conn.cursor()
            cursore.execute(f"INSERT INTO Sensors (dev_id,type_id,mac_RSPi,firmware_version) VALUES ('{id}' , '{t_id}' , '{mac}' , '{f_v}')")
            self.conn.commit()

            return True
        except sq.Error as Er:
            print(f"error : {Er}")
            return False

    def deleteAll(self ,mac):
        

        cursore = self.conn.cursor()
        cursore.execute(f"DELETE FROM Sensors WHERE mac_RSPi = '{mac}'")
        self.conn.commit()

            

    def status(self,mac):
        try:
            
            cursore = self.conn.cursor()
            cursore.execute(f"SELECT mode FROM RSPi WHERE mac == '{mac}'")

            tupla = cursore.fetchone()[0]
            
            
        
        except sq.Error as Er:
            print(f"error : {Er}")
        return tupla

    def updateEvent(self, id, event):
        try:
          
            cursore = self.conn.cursor()
            cursore.execute(f"UPDATE Sensors SET last_event='{event}' , when_last_event='{str(datetime.datetime.now())}' WHERE dev_id='{id}'")

            self.conn.commit()
            
            
        
        except sq.Error as Er:
            print(f"error : {Er}")

    def isSettedAlarm(self, id_s):
        try:
            
            cursore = self.conn.cursor()
            cursore.execute(f"SELECT mode FROM RSPi,Sensors WHERE Sensors.mac_RSPi == RSPi.mac AND Sensors.dev_id == '{id_s}'")

            tupla = cursore.fetchone()
            
            
        
        except sq.Error as Er:
            print(f"error : {Er}")

        if(not tupla):
            print(f"nessun risultato dalla qery:\n SELECT mode FROM RSPi,Sensors WHERE Sensors.mac_RSPi == RSPi.mac AND Sensors.dev_id == '{id_s}'")
        
        if tupla[0] == 2:
            return True
        else:
            return False
    
    def exist(self , id):
        try:
            
            cursore = self.conn.cursor()
            cursore.execute(f"SELECT * FROM Sensors WHERE Sensors.dev_id = '{id}'")

            lista_tuple = cursore.fetchall()
            
            
        
        except sq.Error as Er:
                print(f"error : {Er}")

        if(len(lista_tuple)==0):
            return False
        else:
            return True




    

    def getAll(self , mac):
        try:
            
            cursore = self.conn.cursor()
            cursore.execute(f"SELECT S.* FROM Sensors S , RSPi R WHERE S.mac_RSPi = R.mac AND R.mac = '{mac}'")
            res = cursore.fetchall()
            
            sensors, field_names = res, [i[0] for i in cursore.description] #cursore.description -> index 0 list of list -> field name
       
            sensors_list = resToDict(sensors,field_names)

            return sensors_list
            
        except sq.Error as E:
            print(E)
            return None

    def howManyMac(self , mac):
         try:
            
            cursore = self.conn.cursor()
            cursore.execute(f"SELECT count(*) FROM Sensors WHERE mac_RSPI = '{mac}'")
            count = cursore.fetchone()
            
            return count[0]
         except sq.Error as e:
            print(e)
            return None
        

    def destroy(self):
        self.conn.close()
