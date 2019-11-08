from flask import Flask, jsonify, request
from flask import redirect, url_for
import numpy as np 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# from flask_sqlalchemy import SQLAlchemy 
# from flask_marshmallow import Marshmallow 
import os 
import datetime as dt

#################################################
#  Database  Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Create references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"<h2>Welcome to the Hawaii Weather API!</h2><br/>"
        
        f"<h4>Available API Routes:</h4><br/><br/>"
        
        f"Hawaii Precipitation Data:"
        f"<a href='http://127.0.0.1:5000/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/><br/>"
        f"Hawaii Temperature Observation Data:"
        f"<a href='http://127.0.0.1:5000/api/v1.0/Temp_Observations'>/api/v1.0/temperature_observations</a><br/><br/>"
        f"Hawaii Weather Stations:"
        f"<a href='http://127.0.0.1:5000/api/v1.0/Weather_Stations'>/api/v1.0/weather_stations</a><br/><br/><br/>"      
        f"Hawaii Min, Avg & Max Temps from date entered until today:"
        f"<a href='http://127.0.0.1:5000/api/v1.0/<start_date>'>/api/v1.0/start_date/<start_date><a><br/><br/>"
        f"Hawaii Min, Avg & Max Temps for a specific date range:"
        f"<a href='http://127.0.0.1:5000/api/v1.0/start_date/end_date/<start_date><end_date>'>/api/v1.0/start_date/end_date/<start_date><end_date><a><br/><br/>"
    )
##################################################################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data as json"""
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query precipitation data
    prcp_list_results=session.query(Measurement.date,Measurement.prcp).all()
    session.close()
    
    # Create a dictionary for the precip data 
    precipitation_history=[]
    for date, prcp in prcp_list_results:
        precip_dict = {}
        precip_dict['Date'] = date
        precip_dict['Precipitation (inches)'] = prcp
        precipitation_history.append(precip_dict)
    
    return jsonify (precipitation_history)

#################################################################################################
@app.route("/api/v1.0/Temp_Observations")
def temperature():
    """Return the Temp Observations data as json"""

    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query Temperature data
    tobs_list_results=session.query(Measurement.date,Measurement.tobs).all()
    session.close()
    
    # Create a dictionary for the precip data 
    temperature_history=[]
    for date, tobs in tobs_list_results:
        temp_dict = {}
        temp_dict['Date'] = date
        temp_dict['Temp_Reading (f)'] = tobs
        temperature_history.append(temp_dict)
    
    return jsonify (temperature_history)

# ##################################################################################################
@app.route("/api/v1.0/Weather_Stations")
def weather_stations():
    """Return the Weather_Stations as json"""
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query Weather_Stations data
    weather_station_results=session.query(Station.station, Station.name).group_by(Station.station).order_by(Station.id).all()

    session.close()
    
    # Create a dictionary for the precip data 
    weather_stations=[]
    for station, name in weather_station_results:
        weather_station_dict = {}
        weather_station_dict['station'] = station
        weather_station_dict['name'] = name
        weather_stations.append(weather_station_dict)
    
    return jsonify(weather_stations)

##################################################################################################
##################################################################################################

@app.route("/api/v1.0/start_date")
def temperature_ranges_from_start_date(start_date):
    """Fetch the daily normal temps for the date entered by user."""
    
    #Parse the date 
    St_Date = dt.datetime.strptime(start_date,"%Y-%m-%d")

    # Calculate 
    range_results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.round(func.avg(Measurement.tobs))).\
    filter(Measurement.date >= St_Date).all()

    summary = list(np.ravel(range_results))
    
    # Jsonify summary
    return jsonify(summary)


##################################################################################################
# Two works in progress below for the data for the start and end range of dates
##################################################################################################

# @app.route("/api/v1.0/start_date,end_date/<start_date>/<end_date>/")
# def temperature_ranges_from_start_date(start_date,end_date):
#     """Fetch the daily normal temps for the date entered by user
#        , or a 404 if not."""

#     canonicalized = start_date.replace(" ", "").lower()
#     for temp in calc_temps:
#         search_term = calc_temps["start_date"].replace(" ", "").lower()

#         if search_term == canonicalized:
#             return jsonify(calc_temps)

#     return jsonify({"error": f"calc_temps with start_date {start_date} not found."}), 404

##################################################################################################
# from flask import Flask, request, render_template

# @app.route("/api/v1.0/start_date/end_date/<start_date>/<end_date>")
# def date_range():
#     return render_template('date_range.html')

# @app.route('/get-text', methods=['GET', 'POST'])
# def foo():
#     bar1 = request.form['start_date']
#     bar2 = request.form['end_date']



if __name__ == "__main__":
    app.run(debug=True)

