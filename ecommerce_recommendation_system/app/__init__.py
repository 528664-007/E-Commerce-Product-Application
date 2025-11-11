import os
from flask import Flask
from flask_session import Session
import firebase_admin
from firebase_admin import credentials, firestore

def create_app():
    app = Flask(__name__)

    # === Secret Key and Session Configuration ===
    app.secret_key = os.environ.get("SECRET_KEY", "devkey")
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    Session(app)

    # === Firebase Admin SDK Initialization ===
    cred_path = os.path.abspath("D:\\Coding\\Projects\\ecommerce_recommendation_system\\productrecommenation.json")
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

    # === Register Blueprints ===
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    return app
