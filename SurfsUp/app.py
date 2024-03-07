# Import the dependencies.
import numpy as np
# import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station





#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return all precipitation data"""
    results = session.query(
        Measurement.date,
        Measurement.prcp
    ).all()

    session.close()

    # Convert list to dictionary
    all_prcp = []
    for date,prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return all station data"""
    results = session.query(
        Station.id, 
        Station.station, 
        Station.name,
        Station.latitude,
        Station.longitude,
        Station.elevation
    ).all()

    session.close()

    # Convert list to dictionary
    all_stations = []
    for id,station,name,latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)
    return jsonify(all_stations)
    
@app.route("/api/v1.0/tobs")
def tobs():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return all tobs data for #1 Station"""
    results = session.query(
        Measurement.date, 
        Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.station=='USC00519281').\
    order_by(Measurement.date).all()

    session.close()

    # Convert list to dictionary
    all_tobs = []
    for date,tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)