from ApiFolder import create_main, socketio
from flask import redirect, request,session
from datetime import timedelta
#TODO:
#AGGIUNGERE 'AGGIUNGI RSPI' ALL'HTML
#AGGIUNGERE REGISTRAZIONE PER UTENTI
#NUOVO  COMMENTO
app = create_main()

@app.route('/' , methods=['GET'])
def main():
    if request.method == 'GET':
        return redirect('view')


@app.before_request
def make_session_permanent():
    session.permanent = False
   
app.config['SECRET_KEY'] = 'SECRET!'
if __name__ == '__main__':
    socketio.run(app , port=8000 , host='0.0.0.0')