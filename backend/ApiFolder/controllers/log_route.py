from flask import Flask, Blueprint, request, jsonify
from . import DbLog
from . import DbSensors
from . import DbUsers
import ssl
import smtplib
import datetime

Log = Blueprint('Log',__name__,url_prefix = '/log')
User = DbUsers()
def sendmail(s_id, event):
    message = {
        '01' : 'ALARM! Someone tried to tamper this sensor',
        '02' : 'ALARM! Someone tried to open the door',
        '03' : 'ALARM! Someone tried to tamper this sensor while the door was open',
        '04' : 'Battery low',
        '05' : 'Battery low \n ALARM! Someone tried to tamper this sensor',
        '06' : 'Battery low \n ALARM! Someone tried to open the door',
        '07' : 'Battery low \n ALARM! Someone tried to tamper the door while the door was open',
        '09' : 'ALARM! Detected previous tamper of this sensor, the door is close',
        '0a' : 'ALARM! Door still open',   
        '0b' : 'ALARM! Detected previous tamper of this sensor, the door is open', 
        '0c' : 'Battery low', 
        '0d' : 'Battery low \n ALARM! Detected previous tamper of this sensor, the door is close',
        '0e' : 'Battery low \n ALARM! Detected previus opening of the door',
        '0f' : 'Battery low \n ALARM! Detected previous try to tamper the door while the door was open'
    }
    print(f'receiver: {User.s_idToMail(s_id)}')
    context = ssl.create_default_context()

    sender = "bacobas.f@gmail.com"
    psw = "<password>"
    receiver = f"{User.s_idToMail(s_id)}"
    msg=f"""\
    Object: Sensor alarm {s_id} 


    Sensor id: {s_id}
    Message: {message[event]}
    Messagio python"""

    server= smtplib.SMTP_SSL('smtp.gmail.com' , 465, context=context)

    server.login(sender,psw)
    print("login success ")

    server.sendmail(sender,receiver,msg)
    print("mail sent")
#___________________________



@Log.route('/numberOfLogs', methods = ['POST'])
def numberOfLogs():
    if request.method == "POST":
        id_s = request.get_json(force=True)['id_s']
        if(id_s):
            Log = DbLog()
            num = Log.numberOfLogs(id_s)
            if(num == -1):
                return jsonify({
                'status' : '500' ,
                'message' : 'Invalid id_s'
            })
            else:
                return jsonify({
                'status' : '200' ,
                'message' : f'{num} Logs'
            })
            Log.destroy()
        else:
            return jsonify({
                'status' : '400' ,
                'message' : 'id_s required'
            })

@Log.route('/sensorLogs', methods = ['POST'])
def sensorLogs():
    if request.method == "POST":
        id_s = request.get_json(force=True)['id_s']
    
        Log = DbLog()
        data = Log.sensorLogs(id_s)
        if(data == "Invalid id_s"):
            Log.destroy()

            return jsonify({
            'status' : '500' ,
            'message' : 'Invalid id_s'
            })
        else:

            Log.destroy()
            
            return jsonify({
            'status' : '200' ,
            'data' : data
        })
        

@Log.route('/lastLogs', methods = ['GET'])
def lastLogs():
    if request.method == "GET":
        if 'mac' in request.args:
            mac = request.args['mac']
            Log = DbLog()
            data = Log.lastLogs(mac)
            
            Log.destroy()

            return jsonify({
                'status' : '200' ,
                'data' : data
            })
        else:
            return jsonify({
                'status' : '400' ,
                'message' : 'mac is required'
            })


@Log.route('/insertLog', methods = ['GET'])
def insertLog():
    if request.method == "GET":
        id_s = request.args['id']
        event = request.args['event']
        date = request.args['date']
       
        Sensor = DbSensors()  
        Log = DbLog()
        result = Log.InsertLog(id_s,event,date)

        if not result:
            return 'error with database'

        Log.destroy()

        if(Sensor.isSettedAlarm(id_s) and event!='00' and event != '08'):
            Sensor.destroy()

            sendmail(id_s,event)
            return "alarm"

        else:

            Sensor.destroy()
            return "no alarm"
    else:
        return jsonify({
        'status' : '400',
        'message' : 'invalid request method'
        })


@Log.route('/syncronize' , methods=['POST'])
def syncronize():
    logs = request.get_json(force=True)['logs']
    mac = request.get_json(force=True)['mac']
    
    Log = DbLog()

    logs_list = Log.allLogsMac(mac)

    

    
    print(f'log in db: \n {logs_list}')
    print(f'log in rspi: \n {logs}')
    if(logs_list == logs):
        return "log already sync"
    else:
        Log.deleteAllLogsMac(mac)
        for log in logs:
            Log.InsertLog(log['deviceID'],log['event'],log['whenEvent'])
        return "log syncronized"
    

@Log.route('/all' , methods=['GET'])
def all():
    Log = DbLog()

    return jsonify({
        'status':'200',
        'data' : Log.allLogs()
    })
