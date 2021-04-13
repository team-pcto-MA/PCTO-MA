from flask import Flask, Blueprint, request, render_template, jsonify, jsonify, session, redirect, url_for
from . import DbRSPi
from . import DbUsers
from . import DbSensors
import hashlib
view = Blueprint('view', __name__, url_prefix='/view')

@view.route('' , methods=['GET'])
def home():
    if request.method == 'GET':
        return render_template('home.html')


@view.route('/login' , methods = ['GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')


@view.route('/register' , methods= ['GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

@view.route('/<user>/rspreg' , methods= ['GET'])
def rspireg(user):
    if request.method == 'GET':
        if session['user'] == user:
        
            return render_template('register-rspi.html', user=user)
        else:
            return render_template('error.html' , status='404' , message='not allowed')

@view.route('/<user>', methods = ['GET'])
def user(user):
    print(session)
    if 'user' in session:
        User = DbUsers()
        print(User.found(user))
        if User.found(user):
            if session['user'] == user:
            
                return render_template('user.html')
            else:
                
                return render_template('error.html', status = '404' , message='non cercare di accedere alle paigne di qualcun altro')

        else:
            
            return render_template('error.html', status = '404' , message='utente inesistente')

    else:
        
        return render_template('error.html', status = '404' , message='not logged')


@view.route('/<user>/<rspi>', methods = ['GET'])
def rspi(user, rspi):

    
    if 'user' in session:
        User = DbUsers()
        if User.found(user):
            if session['user'] == user:
                RSPi = DbRSPi()
                if RSPi.existWithOwner(rspi , session['user']):

                    return render_template('rspi.html')
                    
                else:
                     
                    return render_template('error.html' , status='404' , message='you are not the owner of this rspi')   
            else:
                  
                return render_template('error.html', status = '404' , message='non cercare di accedere alle paigne di qualcun altro')
        else:   
            return render_template('error.html', status = '404' , message='utente inesistente')

    else:
        
        return render_template('error.html', status = '404' , message='not logged')


   


