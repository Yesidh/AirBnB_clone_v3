#!usr/bin/python3
'''
flask app module
'''

import os
from models import storage
from flask import Flask, Blueprint
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(exception=None):
    '''
    close session method 
    '''
    storage.close()


if __name__ == '__main__':
    _host = os.getenv('HBNB_API_HOST')
    _port = os.getenv('HBNB_API_PORT')

    app.run(host=_host, port=_port, threaded=True)
