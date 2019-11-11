from flask import Flask, render_template
from flask_socketio import SocketIO, emit
# from flask_sqlalchemy import SQLAlchemy
# from config import Config
# app = Flask(__name__)
# # Config connected via object from config.py
# app.config.from_object(Config)
#
#
# # SocketIO connected
# socketio = SocketIO(app)
#
# # SQL Alchemy connected
# db = SQLAlchemy(app)
#
# # from model.plant_data_model import AppUser

from flask import render_template
from flask_socketio import emit
from flaskr import socketio
from flaskr import app

from flaskr.model.nsrdb_api import getDataFromNSRDB
from flaskr.model.open_weather_api import getWeatherAsJSON
#
# @app.after_request
# def add_header(r):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
#     r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     r.headers["Pragma"] = "no-cache"
#     r.headers["Expires"] = "0"
#     r.headers['Cache-Control'] = 'public, max-age=0'
#     return r

# FLASK ROUTES
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add-user')
def add_user():
    # db.session
    return render_template('home.html')

@app.route('/monitor')
def monitor():
    return render_template('monitor.html')

@app.route('/forecast')
def forecast():
    return render_template('forecast.html')


# SOCKETIO ROUTE
@socketio.on('connect', namespace='/weather')
def test_connect_weather():
    emit('connection response', {'data': 'Weather Connected'})
    print("Response sent")

@socketio.on('connect', namespace='/solar')
def test_connect_solar():
    emit('connection response', {'data': 'Solar Connected'})
    print("Response sent")

@socketio.on('request-weather-data', namespace='/weather')
def get_weather_data(user_request):
    data = getWeatherAsJSON(str(user_request['data']))
    emit('data response', {'data': data})
    print("JSON sent")

@socketio.on('request-solar-data', namespace='/solar')
def get_solar_data(user_request):
    data = getDataFromNSRDB(str(user_request['data']))
    emit('data response', {'data': data})
    print("JSON sent")



# if __name__ == '__main__':
# #     # app.run(debug=True)
# #     socketio.run(app, debug=True)