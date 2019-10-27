from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from model.open_weather_api import getWeatherAsJSON

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
socketio = SocketIO(app)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/monitor')
def monitor():
    return render_template('monitor.html')


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})
    print("Response sent")

@socketio.on('request-server-data', namespace='/test')
def get_weather_data(user_request):
    data = getWeatherAsJSON(str(user_request['data']))
    emit('data response', {'data': data})
    print("JSON sent")


@app.route('/forecast')
def forecast():
    return render_template('forecast.html')

if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app, debug=True)