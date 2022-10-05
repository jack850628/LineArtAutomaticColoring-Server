import sys

import os
from flask import Flask
from flask_cors import CORS
from flaskr.Controllers.api import Coloring
from flaskr.Config import Config
from flask import render_template

def create_app():
    app = Flask(__name__)
    app.debug = Config.DEBUG
    app.config['TESTING'] = Config.TESTING
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    CORS(app, resources={
        r"/api/*": {
            'origins': [
                'http://localhost:8080',
                'http://localhost:8000',
                'https://jack850628.github.io'
            ],
            'methods': [
                'GET',
                'POST',
                'PUT',
                'DELETE',
                'OPTIONS',
            ]
        }
    }) 

    Coloring.init_app(app)


    @app.route("/", methods=['GET'])
    def index():
        return "安安"
        # return render_template("index.html")

    return app