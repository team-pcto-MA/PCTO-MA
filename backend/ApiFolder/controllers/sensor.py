from flask import Flask, Blueprint, request, render_template, jsonify, session, redirect, url_for

import smtplib, ssl, datetime,sqlite3 as sq
from sqlite3 import Error
from . import socketio
from . import DbSensors
from . import DbRSPi

#TODO:
#fix e-mail function
#internet socket



sensor = Blueprint('sensor', __name__, url_prefix='/sensor' )



#GET: update the state of a sensor, if theft protection is setted, it send an e-mail
#POST: register a sensor in database

@sensor.route('' , methods = ['GET' , 'POST'])
def index():
    if request.method == 'GET':
        
        RSPI = DbRSPi()
        SENSOR = DbSensors()
        #get all sensors
        if "mac" in request.args:
            mac = request.args['mac']
            print(mac)
            if(RSPI.ifExists(mac)):
                sensors = SENSOR.getAll(mac)
                
                return jsonify({
                    'status' : '200' ,
                    'lenght' : len(sensors) ,
                    'data' : sensors
                })
            else:
                return jsonify({
                'status' : '500' , 
                'message' : 'RSPi not registred'
                })
        else:
            return jsonify({
                'status' : '400' , 
                'message' : 'Mac required'
                })

    elif request.method == 'POST':
        mac = request.get_json(force = True)['mac']
        id = request.get_json(force = True)['id']
        type_id = request.get_json(force = True)['type_id']
        firm_ver = request.get_json(force = True)['firm_ver']
        
    #------------------
        registrator = DbSensors()
        if registrator.addSensor(mac,id,type_id,firm_ver):
            return "signed up sensor"
        else:
            return "sensor exist"

        registrator.destroy()
    #---------------------

    else:
        return jsonify({
            'status' : '400',
            'message' : 'invalid request method'
        })


#say if a sensor with this id exist
@sensor.route('/check' , methods = ['GET' , 'POST'])#used by rspi
def check(): 
    if request.method == 'POST':
        id = request.get_json(force=True)['id']
        
        Sensor = DbSensors()
        if(Sensor.exist(id)):
            return "exist"
        else:
            return "not exist"
    else:
        return jsonify({
            'status' : '400',
            'message' : 'invalid request method'
        })
        

        
@sensor.route('/syncro_req' , methods=['POST'])
def syncroreq():
    mac = request.get_json(force = True)['mac']
    print(mac)
    
    
    socketio.emit('syncronize',{'mac' : mac})
    return 'ok'

    
    
    

@sensor.route('/syncronize' , methods=['POST'])
def syncronize():
    sensors = request.get_json(force=True)['sensors']
    mac = request.get_json(force=True)['mac']
    
    Sensor = DbSensors()
    id_db = []
    id_rspi = []

    dbsensors, field_names = Sensor.getAll(mac)
    sensors_list = []
    if(len(dbsensors) != 0 or dbsensors != None):
        for dbsensor in dbsensors: #sensor -> number of elements x sensor, every sensor has 6 values
            count = 0
            sensor_dict = {} #last sensor
            for field in field_names: #number of fields
                sensor_dict[f'{field}'] = dbsensor[count] #matching fields to corresponding sensors
                count += 1 #moving to the next value of the corresponding sensor, 1 - 2 - 3 - 4 - 5 - 6
            sensors_list.append(sensor_dict) #final dict of sensors, sensor "number" -> corresponding dict of values




    for dbsensor in sensors_list:
        id_db.append(dbsensor['dev_id'])


    for sensor in sensors:
        id_rspi.append(sensor['DEVICE_ID'])

    id_rspi.sort()
    id_db.sort()
    print(f'rspi: {id_rspi}')
    print(f'db: {id_db}')
    print(id_db == id_rspi)
    
    if (id_db == id_rspi):
        Sensor.destroy()
        return 'not syincronized'
         
    else:
        try:
            Sensor.deleteAll(mac)
            for sensor in sensors:
                Sensor.addSensor(mac , sensor['DEVICE_ID'], sensor['TYPE_ID'], sensor['FIRMWARE_VERSION'])
            
        except Error as e:
            print(e)
        Sensor.destroy()
        return 'syincronized'

    
