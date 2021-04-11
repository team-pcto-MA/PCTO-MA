import sqlite3 as sq
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

class DbRSPi:
    def __init__(self):
        self.conn = sq.connect('MA_002.db')
        self.table = 'RSPi'
    
    def ifExists(self, mac):
        try:
            cursore = self.conn.cursor()
            cursore.execute(f"SELECT DISTINCT mac FROM RSPi WHERE RSPi.mac == '{mac}'")

        except sq.Error as er:
            print(f"Error -> {er}")
        
        if(cursore.fetchone()):
            return True
        else:
            return False

    def changeMode(self,mac,mode):
        
        cursore = self.conn.cursor()
        cursore.execute(f"UPDATE {self.table} SET mode = '{mode}' WHERE mac = '{mac}'")
        self.conn.commit()
        

    def readMode(self,mac):
        try:    
            cursore = self.conn.cursor()
            cursore.execute(f"SELECT mode FROM RSPi WHERE mac == '{mac}'")
            result = cursore.fetchone()
        except sq.Error as Er:
            print(f"Error -> {Er}")
        return result

    def getInfo(self,mac):
        try:
            cursore = self.conn.cursor()
            cursore.execute(f"SELECT * FROM RSPi WHERE mac == '{mac}'")
            fields = [i[0] for i in cursore.description]
            results = cursore.fetchone()
        except sq.Error as Er:
            print(f"Error -> {Er}")
        return results,fields

    def addRSPi(self,mac , user):
        
        cursore = self.conn.cursor()
        cursore.execute(f"INSERT INTO RSPi (mac , user) VALUES ('{mac}','{user}')")
        self.conn.commit()
        


    def existWithOwner(self, mac, user):
        try:
            cursore = self.conn.cursor()
            cursore.execute(f"SELECT * FROM RSPi WHERE mac = '{mac}' AND user = '{user}'")
            results = cursore.fetchone()
            if results:
                return True
            else:
                return False

        except sq.Error as Er:
            print(f"Error -> {Er}")
            return False

    def getAll(self , user):
        try:
            
            cursore = self.conn.cursor()
            print(f"SELECT * FROM RSPi WHERE user = '{user}'")
            cursore.execute(f"SELECT * FROM RSPi WHERE user = '{user}'")
            sensors = cursore.fetchall()
            
            return resToDict (sensors, [i[0] for i in cursore.description]) #cursore.description -> index 0 list of list -> field name
        except sq.Error as E:
            print(f'error: {E}')
            return None

    def destroy(self):
        self.conn.close()