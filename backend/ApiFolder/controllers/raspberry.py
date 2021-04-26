from flask import Flask, Blueprint, request, jsonify,session
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from . import DbRSPi
from . import socketio
import sqlite3 as sq
RSPi = Blueprint('RSPi',__name__,url_prefix='/RSPi')

@RSPi.route('/ifExists', methods = ['POST'])
def ifExists():
    if request.method == 'POST':
        mac = request.get_json(force=True)['mac']
        if(mac):
            Raspberry = DbRSPi()
            if(Raspberry.ifExists(mac)):
                return jsonify({
                    'status' : '200' ,
                    'message' : 'Exists'
                })
            else:
                return jsonify({
                    'status' : '500' ,
                    'message' : 'RSPi not in db'
                })
            Raspberry.destroy()
        else:
            return jsonify({
                    'status' : '400' ,
                    'message' : 'Mac required'
                })

@RSPi.route('/readMode', methods = ['POST']) # from rspi
def readMode():
    if request.method == 'POST':
        mac = request.get_json(force=True)['mac']
        Raspberry = DbRSPi()
        try:
            mode = Raspberry.readMode(mac)[0]
            Raspberry.destroy()
            return str(mode)
        except:
            return "RSPi not exist"

@RSPi.route('/changeMode', methods = ['POST'])
def changeMode():
    if request.method == 'POST':
        mac = request.get_json(force=True)['mac']
        mode = request.get_json(force=True)['mode']
        #print(session["user"])
        Raspberry = DbRSPi()
        if(mac and mode):
            if session:
                if Raspberry.existWithOwner(mac, session['user']):
                    
                    try:
                        Raspberry.changeMode(mac,mode)

                        return jsonify({
                            'status' : '200',
                            'message' : f'mode changed to {mode}'
                        })
                    except sq.Error as E:
                        return jsonify({
                            'status' : '400',
                            'message' : f'Change mode error: {E}'
                        })
                    Raspberry.destroy()
                else:
                    return jsonify({
                        'status' : '400' ,
                        'message' : 'You are not the owner!'
                    })
            else:
                return jsonify({
                        'status' : '400' ,
                        'message' : 'You are not logged'
                    })

        else:
            return jsonify({
                    'status' : '400' ,
                    'message' : 'Mac & mode required'
                })

@RSPi.route('/getInfo', methods = ['POST'])
def getInfo():
    if request.method == 'POST':
        mac = request.get_json(force=True)['mac']
        if(mac):
            Raspberry = DbRSPi()
            

            if session:
                if Raspberry.existWithOwner(mac, session['user']):
                    
                    try:
                        Raspberry = DbRSPi()
                        results, fields = Raspberry.getInfo(mac)
                        dictionary = {}
                        count = 0
                        for result in results:
                            dictionary[f'{fields[count]}'] = result
                            count += 1
                        Raspberry.destroy()
                        return jsonify({
                            'status' : '200',
                            'info' : dictionary
                        })
                    except:
                        return jsonify({
                            'status' : '400',
                            'message' : 'Get info error'
                        })
                    Raspberry.destroy()
                else:
                    return jsonify({
                        'status' : '400' ,
                        'message' : 'You are not the owner!'
                    })
            else:
                return jsonify({
                        'status' : '400' ,
                        'message' : 'You are not logged'
                    })

        else:
            return jsonify({
                    'status' : '400' ,
                    'message' : 'Mac & mode required'
                })








@RSPi.route('/sendMode', methods = ['POST'])
def sendMode():
    mac = request.get_json(force = True)['mac']
    mode = request.get_json(force = True)['mode']
    print(mac)
    print(mode)
    try:
        socketio.emit('new_mode',{'mac' : mac, 'mode' : mode})
        return 'ok'

    except:
        return 'not ok'

@RSPi.route('', methods = ['POST', 'GET'])
def add():
    if request.method == 'POST':
        mac = request.get_json(force = True)['mac']
        user = request.get_json(force = True)['user']
        name = request.get_json(force = True)['name']
        
        print(mac)
        print(user)
        RSPI = DbRSPi()
        try:
            RSPI.addRSPi(mac, user, name)
            return jsonify({
                'status' : '200',
                'message' : 'added new RSPi'
            })
        except sq.Error as E:
            return jsonify({
                'status' : '500',
                'message' : f'{E}'
            })
    else:
        if 'user' in request.args:

            user = request.args['user']
            RSPi = DbRSPi()
            data = RSPi.getAll(user)
            print(data)
            return jsonify({
                'status' : '200',
                'data' : data
                })
        else:
            return jsonify({
                'status' : '400',
                'message' : 'must ask for a user!'
            })


@RSPi.route('/setName' , methods = ['PATCH'])
def setName():
    mac = request.get_json(force = True)['mac']
    name = request.get_json(force = True)['name']
    ownerName = request.get_json(force = True)['ownerName']
    RSPI = DbRSPi()
    print(session)
    if session:

        if RSPI.existWithOwner(mac , ownerName):
            try:
                RSPI.updateName(mac,name)
                return jsonify({
                    'status' : '200',
                    'message' : 'succesfully changed name!'
                })
            except sq.Error as E:
                print(f'error : {E}')
                return jsonify({
                    'status' : '500',
                    'message' : 'something went wrong!'
                })
        else:
            return jsonify({
                    'status' : '400',
                    'message' : "you can't change the nema of a rspi that you not got"
                }) 
    else:
        return jsonify({
                    'status' : '400',
                    'message' : "you're not logged"
                }) 








  