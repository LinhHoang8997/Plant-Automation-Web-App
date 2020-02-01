from flask import render_template, redirect, url_for, flash
from flask_socketio import emit

# Import components from root
from flaskr import app
from flaskr import db
from flaskr import socketio

from flask_login import current_user, login_user
from flaskr.model.plant_data_model import AppUser, LoginForm
from flaskr.model.nsrdb_api import getDataFromNSRDB
from flaskr.model.open_weather_api import getWeatherAsJSON
from sqlalchemy import text
from sqlalchemy.sql import select

import pandas as pd

from sqlite3 import OperationalError
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
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    # form.content(style="", class_="form-control")
    if form.validate_on_submit():
        user = AppUser.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/')
def home():
    return render_template('home.html')

def start_server():
    socketio.run(app)

@app.route('/add-user')
def add_user():
    # db.session
    return render_template('home.html')

@app.route('/monitor')
def monitor():
    #For demo purposes -> We are using dthormann1 - #2
    demo_username = 'dthormann1' #Proper log-in mechanism to be implemented soon
    # get_id_query = "SELECT
    query_result = db.session.query(AppUser.UserID).filter_by(Username = demo_username).first()
    demo_userid = query_result.UserID
    print(demo_userid)

    # For practice purposes, SQLAlchemy's Textual SQL is used. However, using the ORM's provided methods will provide more security
    plot_info_query = text('''
    SELECT
    AppUser.Username, AppUser.DateJoined, AppUser.RoleID, PlotInfo. *, PlotTypes.PlotTypeDescription, PlantEncyclopedia.PlantName
        FROM AppUser 
            INNER JOIN PlotInfo USING(UserID)
            LEFT JOIN PlotTypes USING(PlotTypeID)
            LEFT JOIN PlantEncyclopedia USING(PlantID)
        WHERE UserID = :userid ''')

    plot_info_overview_data = db.engine.execute(plot_info_query, userid=demo_userid).fetchall()

    # NOTE: OUTPUT COLUMN IS ONLY TEMPORARY - DESIGN SHOULD CHANGE LATER

    return render_template('monitor.html', demo_username=demo_username, data=plot_info_overview_data)

@app.route('/admin-view')
def admin_view():
    sql_query = text('select Username, Email from AppUser')
    data_fetched = db.engine.execute(sql_query).fetchall()
    list_of_username = [item['Username'] for item in data_fetched]

    # If admin does not exist on the database yet
    if "admin" not in list_of_username:
        admin = AppUser(Username='admin', Email='admin@example.com', RoleID=1)
        admin.set_password("TestPassword")
        admin.get_current_date()
        db.session.add(admin)
        db.session.commit()
        db.session.close()
    # else:
    #     db.session.commit()
    #     db.session.close()

    # try:
    #     db.engine.connect()
    #     result = db.engine.execute(sql_query)
    # except OperationalError:
    #     db.create_all()
    #     admin = AppUser(username='admin', email='admin@example.com')
    #     guest = AppUser(username='guest', email='guest@example.com')
    #     db.session.add(admin)
    #     db.session.add(guest)
    #     db.session.commit()
    #     result = AppUser.query.all()

    return render_template('admin_view.html', data=data_fetched)

@app.route('/forecast')
def forecast():
    return render_template('forecast.html')

# SOCKETIO ROUTE
@socketio.on('connect', namespace='/weather')
def test_connect_weather():
    emit('connection response', {'data': 'Weather Connected'})
    print("Connection confirmation sent")

@socketio.on('request-weather-data', namespace='/weather')
def get_weather_data(user_request):
    data = getWeatherAsJSON(str(user_request['data']))
    emit('data response', {'data': data})
    print("JSON sent")

@socketio.on('connect', namespace='/solar')
def test_connect_solar():
    emit('connection response', {'data': 'Solar Connected'})
    print("Connection confirmation sent")


@socketio.on('request-solar-data', namespace='/solar')
def get_solar_data(user_request):
    print("JSON sent")
    data = getDataFromNSRDB(str(user_request['data']))
    emit('data response', {'data': data})
    print("JSON sent")

@socketio.on('connect', namespace='/get_monitor_data')
def test_connect_monitor():
    emit('connection response', {'data': 'Monitor Connected'})
    print("Connection confirmation sent")


@socketio.on('request-monitor-data', namespace='/get_monitor_data')
def get_monitor_data():
    # Should refactor so naming is consistent
    demo_username = 'dthormann1'  # Proper log-in mechanism to be implemented soon
    query_result = db.session.query(AppUser.UserID).filter_by(Username=demo_username).first()
    demo_userid = query_result.UserID
    plot_info_query = text('''
        SELECT
        PlotInfo. *, PlotTypes.PlotTypeDescription, PlantEncyclopedia.PlantName, OutputSum
            FROM AppUser 
                INNER JOIN PlotInfo USING(UserID)
                LEFT JOIN PlotTypes USING(PlotTypeID)
                LEFT JOIN PlantEncyclopedia USING(PlantID)
                LEFT JOIN 
                    (SELECT PlotID, SUM(OutputValue) AS OutputSum
                    FROM OutputLog 
                    WHERE datetime(Date,'unixepoch') BETWEEN datetime("now", '-3 months') AND datetime("now", 'start of day')
                    GROUP BY PlotID)
                USING(PlotID)
            WHERE UserID = :userid ''')
    cursor = db.engine.execute(plot_info_query, userid=demo_userid)
    plot_info_all_data = pd.DataFrame.from_records([dict(row.items()) for row in cursor.fetchall()])
    plot_info_all_data_json = plot_info_all_data.to_json(orient='records')
    # Or use this row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}
    print(plot_info_all_data_json)

    by_plant_data = plot_info_all_data.groupby('PlantName').sum().reset_index()[['PlantName','OutputSum']]
    by_plant_data.loc[:, 'PlantName'] = by_plant_data['PlantName'].str.split(pat=',', expand=True)[0]
    by_plant_data.reset_index(inplace=True)
    by_plant_data.columns = ['id', 'x', 'y']
    by_plant_data_json = by_plant_data.to_json(orient='records')
    print(by_plant_data_json)

    cursor.close()
    emit('data response', {'message': 'Monitor Connected', 'all_data': plot_info_all_data_json, 'plant_data': by_plant_data_json})
    print("Response sent")




# if __name__ == '__main__':
# #     # app.run(debug=True)
# #     socketio.run(app, debug=True)