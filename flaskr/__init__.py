from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
from flaskr.config import Config

app = Flask(__name__)
# Config connected via object from config.py
app.config.from_object(Config)

# Initialized Login Manager
login_manager = LoginManager(app)


# SocketIO connected
socketio = SocketIO(app, async_mode="threading")

# SQL Alchemy connected
db = SQLAlchemy(app)

# from model.plant_data_model import AppUser

from flaskr import routes
# from flaskr.model import plant_data_model

# if __name__ == '__main__':
#     # app.run(debug=True)
#     app.run(debug=True, port=8080)