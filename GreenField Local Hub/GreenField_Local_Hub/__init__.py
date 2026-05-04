from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecret123'  

    from .views import main_bp
    app.register_blueprint(main_bp)

    return app
