from flask import Flask,session
from flask_socketio import SocketIO

socketio = SocketIO()
from .models.raspberry import DbRSPi
from .models.sensors import DbSensors
from .models.users import DbUsers
from .models.log import DbLog


def create_main():
    global socketio
    app = Flask(__name__ , static_folder="../static", template_folder='../templates')
    from .controllers.sensor import sensor
    from .controllers.user import user
    from .controllers.raspberry import RSPi
    from .controllers.view import view
    from .controllers.log_route import Log
    socketio.init_app(app)

    app.register_blueprint(user)
    app.register_blueprint(view)
    app.register_blueprint(Log)
    
    app.register_blueprint(sensor)
    app.register_blueprint(RSPi)
    app.debug = True
    
    
    
    
    return app