from flask import Flask


def create_main():
    app = Flask(__name__)

    from .login import login

    app.register_blueprint(login, urlprefix='/')

    
    return app