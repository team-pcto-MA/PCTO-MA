from flask import Flask, Blueprint, request, render_template, jsonify, jsonify


RSPi = Blueprint('RSPi', __name__, url_prefix='/RSPi' )

@RSPi.route('/scan' , methods= ['GET' , 'POST'])
def index():
    if request.method == 'POST':
        s_name = request.get_json(force=True)['name'] #nome sensore
        s_mac = request.get_json(force=True)['mac'] #mac sensore
        # s_prop = request.get_json(force=True)['ownerName'] #nome proprietario
        # inserisci sensore nella tabella dei sensori -> inserisci_s(s_name,s_mac)
    elif request.method == 'GET':

        if not request.args:
            #dizionario_sensori = funzione che prende tutti i sensori dalla tabella dei sensori

            return jsonify({
                'status' : 'success',
                'data' : '<dizionario sensori>'
                })

        elif len(request.args)==1 and request.args['id']:
            #sensore = funzione che ritorna un dizionario contenente il mac e il nome del senore (l'intero record di quel sensore)
            return jsonify({
                'status' : 'success' ,
                'data' : '<sensore>'
            })
        else:
            return jsonify({
                'status' : 'error' ,
                'data' : 'parametri non validi'
            })
    else:
        return jsonify({
                'status' : 'error' ,
                'data' : 'metodo non valido'
            })

       
    