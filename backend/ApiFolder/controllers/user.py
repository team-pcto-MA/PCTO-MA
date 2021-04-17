from flask import Flask, Blueprint, request, render_template, jsonify, jsonify, session, redirect, url_for
from . import DbUsers
import hashlib
user = Blueprint('user', __name__, url_prefix='/user' )





@user.route('' , methods= ['GET' , 'POST'])
def index():
    if request.method == 'GET':
        if not request.args:


            if session:
                
                    
                try:
                    User = DbUsers()
                    results, fields = User.getInfo(session['user'])
                    dictionary = {}
                    count = 0
                    for result in results:
                        dictionary[f'{fields[count]}'] = result
                        count += 1
                    User.destroy()
                    return jsonify({
                        'status' : '200',
                        'data' : dictionary
                    })
                except:
                    return jsonify({
                        'status' : '400',
                        'message' : 'Get info error'
                    })
                User.destroy()
                
            else:
                return jsonify({
                        'status' : '400' ,
                        'message' : 'You are not logged'
                    })



        elif len(request.args)==1 and 'username' in request.args:
            User = DbUsers()
            if session:
                if session['user']=='admin':
                    
                    try:
                        
                        results, fields = User.getInfo(request.args['username'])
                        dictionary = {}
                        count = 0
                        for result in results:
                            dictionary[f'{fields[count]}'] = result
                            count += 1
                        User.destroy()
                        return jsonify({
                            'status' : '200',
                            'info' : dictionary
                        })
                    except:
                        return jsonify({
                            'status' : '400',
                            'message' : 'Get info error'
                        })
                    User.destroy()
                else:
                    return jsonify({
                        'status' : '400' ,
                        'message' : 'You are not the admin! If you want your information try to /user/'
                    })
            else:
                return jsonify({
                        'status' : '400' ,
                        'message' : 'You are not logged'
                    })














            return jsonify({
                'status' : 'fail' , 
                'message' : f"api_get_user_{request.args['id']}"
                })
        else:
            return jsonify({
                'status' : 'error' 
            , 'message' : 'bad_request'
            })
    elif request.method == 'POST':
        psw = request.form['psw']
        psw1 = request.form['psw1']
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        name = request.form['name']
        surname = request.form['surname']
        if(psw and psw and username and email and name and surname):
            User = DbUsers()

            res = User.register(hashlib.md5(psw.encode()).hexdigest(), hashlib.md5(psw1.encode()).hexdigest() , username, email , phone, name , surname)

            User.destroy()
            return jsonify(res)
        else:
            return jsonify({
                'status' : '400' , 
                'message' : 'you must insert all obbligatory fields'
            })

    else:
        return jsonify({
            'status' : '400' , 
            'message' : 'bad request method'
            })


@user.route('/login' , methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        try:  #se inviati da un form
            username = request.form['user'] 
            psw = request.form['psw'] 
        except:  #se non inviati da un form
            username = request.get_json(force=True)['user'] 
            psw = request.get_json(force=True)['psw'] 

        User = DbUsers()
        if User.login(hashlib.md5(psw.encode()).hexdigest() , username):
            User.destroy()
            session['logged'] = True
            session['user'] = username

            return jsonify({
                'status' : '200',
                'message' : 'done'
            })
        else:
            return jsonify({
            'status' : '400',
            'message' : 'bad credentials'
            })

    else:
        #pagina di loggin
        return jsonify({
        'status' : '400', 
        'message' : 'bad request method'
        })


@user.route('/loginJson' , methods = ['POST','GET'])


@user.route('/secret' , methods = ['POST', 'GET'])
def secret():
    if request.method == 'GET':
        if session.get('logged'):
            return f"<h1>Secret page {session['user']}</h1>"
        else:
            return "<h1>not logged</h1>"

    else:

        return jsonify({
            'status' : '404', 
            'message' : 'bad request method'
        })

@user.route('/logOut' , methods = ['POST', 'GET'])
def clearSession():
    if request.method == 'GET':
        
        session.clear()
        return jsonify({
            'status' : '200', 
            'message' : 'session erased'
        })
    else:
        return jsonify({
            'status' : '404', 
            'message' : 'bad request method'
        })



