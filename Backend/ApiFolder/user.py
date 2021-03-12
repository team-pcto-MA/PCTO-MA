from flask import Flask, Blueprint, request, render_template, jsonify, jsonify


user = Blueprint('user', __name__, url_prefix='/user' )

@user.route('/' , methods= ['GET' , 'POST'])
def index():
    if request.method == 'GET':
        if not request.args:
            return jsonify({'status' : 'fail' , 'message' : 'api_get_all_users'})
        elif len(request.args)==1 and request.args['id']:
            return jsonify({'status' : 'fail' , 'message' : f"api_get_user_{request.args['id']}"})
        else:
            return jsonify({'status' : 'error' , 'message' : 'bad_request'})
    elif request.method == 'POST':
        #funzione che crea nuovo utente: addUser()
        return jsonify({'status' : 'success' , 'utente_creato' : '<tutti i dati dell utente creato>' })
    else:
        return jsonify({'status' : 'fail' , 'message' : 'metodo_url non valido'})




