#!usr/bin/python3
'''
Index module
'''

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    '''
    Status method
    '''
    return jsonify({'status': 'OK'})