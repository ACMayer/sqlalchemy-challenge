import numpy as np
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
import datetime as dt
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database intso a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement
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
        f"/api/v1.0/temp/<start><br/>"
        f"/api/v1.0/temp/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
     # Calculate the date 1 year ago from last date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query all precipitation
    results = session.query(Measurement.date,Measurement.prcp ).filter(Measurement.date >= prev_year).all()
    #Close a session
    session.close()
    # Create a dictionary from the row data and append to a list of all precipitation   
    all_precipitation = {date: prcp for date, prcp in results}
    #Return JSON List
    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    resultsstations = session.query(Station.station).all()
    #Close a session
    session.close()

   # Convert list of tuples into normal list
    station_list = list(np.ravel(resultsstations))
    #Return JSON List
    return jsonify(station_list=station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Calculate the date 1 year ago from last date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query all temps of Station ID: USC00519281 the most active station
    tobsresults = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station =="USC00519281").filter(Measurement.date >= prev_year).all()
    #Close a session
    session.close()
    all_tobs = {date: tobs for date, tobs in tobsresults}
    #Return JSON List
    return jsonify(all_tobs)



@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    if not end:
        session = Session(engine)
        start = dt.datetime.strptime(start, "%Y%m%d")
        results=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
        #Close a session
        session.close()
        # Convert list of tuples into normal list
        results_list = list(np.ravel(results))
        return jsonify(results_list)
    start = dt.datetime.strptime(start, "%Y%m%d")
    end = dt.datetime.strptime(end, "%Y%m%d")
# Create our session (link) from Python to the DB
    session = Session(engine)
    #Query with functions
    results= session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    #Close a session
    session.close()
    # Convert list of tuples into normal list
    results_list = list(np.ravel(results))
    return jsonify(results_list)
   

if __name__ == '__main__':
    app.run(debug=True)
