# -*- coding: utf-8 -*-
from flask import Flask


def create_app():
    app = Flask(__name__.split('.')[0], instance_relative_config=True)
    # app.config.from_object('config')
    # app.config.from_pyfile('config.py', silent=True)

    return app
