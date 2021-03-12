from flask import Flask


def create_main():
    app = Flask(__name__)

    from .user import user
    from .RSPi import RSPi
    app.register_blueprint(user)
    app.register_blueprint(RSPi)

    
    return app