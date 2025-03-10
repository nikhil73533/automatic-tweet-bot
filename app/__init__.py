from flask import Flask
from app.routes import main_bp
import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)

    app.register_blueprint(main_bp)

    #Loading environment variables.
    load_dotenv("/home/mockingj/New Drive/Personal Projects/tweet_app/app/secrets.env")

    return app
