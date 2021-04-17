from ApiFolder import create_main, socketio
from flask import redirect, request,session
from datetime import timedelta

app = create_main()
rspi = []
@app.route('/' , methods=['GET'])
def main():
    if request.method == 'GET':
        return redirect('view')


@socketio.on('newrspi')
def connect(mac):
    print(f'NUOVO CLIENT CON MAC : {mac}')
    rspi.append({mac : request.sid})
    print(rspi)


@socketio.on('disconnect')
def desconnect():
    print(f'{request.sid} DISCONNESSO')
    del rspi[request.sid]
    print(rspi)


@app.before_request
def make_session_permanent():
    session.permanent = False
   
app.config['SECRET_KEY'] = 'SECRET!'
if __name__ == '__main__':
    socketio.run(app , port=8000 , host='0.0.0.0')