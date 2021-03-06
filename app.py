# facilitate ORM...
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# refelct existing database into new model
Base = automap_base()

# reflect tables
Base.prepare(engine, reflect=True)

# save references
Measurements = Base.classes.measurement
Stations = Base.classes.station

# Flask setup
app = Flask(__name__)


####################################################
# Routes
####################################################

# Homepage route
@app.route("/")
def home():
    return (f"Welcome to my SQLAlchemy HW API!<br/>"
            f"<br/>"
            f"Available Routes: <br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/start (format = YYYY-MM-DD)<br/>"
            f"/api/v1.0/start/end (format = YYYY-MM-DD)")


# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    # query results
    results = session.query(Measurements.date, Measurements.prcp).filter(Measurements.date >= '2016-08-23').all()

    session.close()

    # create a dictionary and jsonify the results
    precipitation_data = []
    for date, precip in results:
        precipitation_dict = {}
        precipitation_dict["Date"] = date
        precipitation_dict["Precipitation (Inches)"] = precip
        precipitation_data.append(precipitation_dict)

    return jsonify(precipitation_data)


# Stations route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    # query results
    results = session.query(Stations.station, Stations.name).all()

    session.close()

    # return json list of stations from the dataset
    stations_list = []
    for station_id, location in results:
        stations_dict = {}
        stations_dict["Station ID"] = station_id
        stations_dict["Location"] = location
        stations_list.append(stations_dict)

    return jsonify(stations_list)


# Temperatures route
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # query results
    results = session.query(Measurements.station, Measurements.date, Measurements.tobs).filter(Measurements.station == "USC00519281").\
              filter(Measurements.date >= "2016-08-23").all()

    session.close()

    # return JSON list of temperatures from last year
    temps_list = []
    for station_id, date, temp in results:
        temps_dict = {}
        temps_dict["Station ID"] = station_id
        temps_dict["Date"] = date
        temps_dict["Temperature (F)"] = temp
        temps_list.append(temps_dict)

    return jsonify(temps_list)


# Start route
@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)

    # query results
    results = session.query(Measurements.date, func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
              filter(Measurements.date >= start).group_by(Measurements.date).all()

    session.close()

    # create disctionary and return results as json
    start_date = []
    for date, tmin, tavg, tmax in results:
        start_dates = {}
        start_dates["Date"] = date
        start_dates["Tmin"] = tmin
        start_dates["Tavg"] = tavg
        start_dates["Tmax"] = tmax
        start_date.append(start_dates)

    return jsonify(start_date)


# Start End route
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    session = Session(engine)

    # query results
    results = session.query(Measurements.date, func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
              filter(Measurements.date >= start).filter(Measurements.date <= end).group_by(Measurements.date).all()

    session.close()

    # create disctionary and return results as json
    start_end_date = []
    for date, tmin, tavg, tmax in results:
        start_end_dates = {}
        start_end_dates["Date"] = date
        start_end_dates["Tmin"] = tmin
        start_end_dates["Tavg"] = tavg
        start_end_dates["Tmax"] = tmax
        start_end_date.append(start_end_dates)

    return jsonify(start_end_date)


if __name__ == "__main__":
    app.run(debug=True)
