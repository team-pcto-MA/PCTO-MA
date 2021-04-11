import sqlite3 as sq
from sqlite3 import Error


class DbUsers:
    def __init__(self):
        self.conn = sq.connect('MA_002.db' , check_same_thread=False)
        self.table = 'Users'
    def openConn(self):
        self.conn = sq.connect('MA_002.db' , check_same_thread=False)
    def found(self , username):
        try:
            cursor = self.conn.cursor()
            query = f"SELECT * FROM {self.table} WHERE username = '{username}'"
            print(query)
            cursor.execute(query)

            if (cursor.fetchone()):
                return True
            else:
                return False
        except:
            return False

    def getInfo(self,user):
        try:
            cursore = self.conn.cursor()
            cursore.execute(f"SELECT * FROM Users WHERE username == '{user}'")
            fields = [i[0] for i in cursore.description]
            results = cursore.fetchone()
        except sq.Error as Er:
            print(f"Error -> {Er}")
        return results,fields

    def login(self , psw , username):
        try:
            cursor = self.conn.cursor()
            query = f"SELECT * FROM {self.table} WHERE username = '{username}' AND psw = '{psw}'"
            cursor.execute(query)

            if (cursor.fetchone()):
                return True
            else:
                return False
        except sq.Error as E:
            print(f'error: {E}')
            return False

    def register(self, psw, psw1, username,email,phone,name,surname):

        if psw == psw1:
            try:
                if not self.found(username):
                    cursor = self.conn.cursor()
                    query = f"INSERT INTO Users (username,psw,email,phone,name,surname) VALUES ('{username}','{psw}','{email}','{phone}','{name}','{surname}')"
                    cursor.execute(query)

                    self.conn.commit()
                    return {
                        'status' : '200',
                        'message' : 'done'
                        }
                else:
                    return {
                        'status' : '400',
                        'message' : 'user exist'
                    }
            except sq.Error as E:
                print(E)
                return {
                    'status' : '500',
                    'message' : f'Error : {E}'
                }
        else:
            return {
                'status' : '400',
                'message' : 'psw not equals'
            }
    def s_idToMail(self , s_id):
        try:
            cursor = self.conn.cursor()
            query = f"SELECT email FROM Sensors, RSPi, Users WHERE Sensors.mac_RSPi = RSPi.mac AND Users.username = RSPi.user  AND dev_id = '{s_id}'"
            cursor.execute(query)
            res = cursor.fetchone()
            if (res):
                return res[0]
            else:
                return False
        except sq.Error as E:
            print(f'error: {E}')
            return False

    def destroy(self):
        self.conn.close()