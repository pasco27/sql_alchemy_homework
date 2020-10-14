
## This is a flast app for the SQLAlchemy HW
## Using the titanic app class example as a base document


import numpy as np
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Route
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to Beautiful Hawaii!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temps/<start><br/>"
        f"/api/v1.0/temps/<start>/<end><br/>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    # Convert query results to a dict using date as the key and prcp as the value
    
    # Query the database
    session = Session(engine)
    precip = session.query(measurement.date, measurement.prcp).filter(measurement.date).all()
    # close the session to end communication with the server
    session.close()

    # create the dict that will be jsonified of date and prcp
    hawaii_measurements = []
    for dates in precip:
        measurements = {}
        measurement['date'] = measurement.date
        measurement['precipitaion'] = measurement.prcp
        hawaii_measurements.append(measurements)   
    
    
    # all_locs_prcp = list(np.ravel(results))
    # alternative with list comprehension
    # all_names = [result[0] for result in results]

    return jsonify(hawaii_measurements)


@app.route('/api/v1.0/stations')
def stations():

    # Return a JSON list of stations from the dataset 
    
    # Query the database
    session = Session(engine)
    station_count = session.query(measurement.station).group_by(measurement.station).all()
    # close session
    session.close()
   
    # ???
    return jsonify(station_count)


@app.route('/api/v1.0/tobs')
def tobs():
    # Query the dates and temperature observations of the most active station for the last year of data.
    # for simplicity of the exercise I know from the precip analysis portion that most active == USC00519281 
    
    # Query the database
    session = Session(engine)
    ## This was for MIN, from the last exercise 
    lowest2 = session.query(measurement.station, func.min(measurement.tobs).label('min')).filter(measurement.station=='USC00519281').all()
    past_year = session.query(measurement.date, measurement.prcp).filter(measurement.date >= "2016-08-23").all()
    # close session
    session.close()    
    
    return jsonify(...whatever I decide to call this...)







@app.route('/api/v1.0/start')
def start():
    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date
    
    # Query the database
    session = Session(engine)
    #############station_count = session.query(measurement.station).group_by(measurement.station).all()
    # close session
    session.close()
    
    return (
        some stuff....
    )


@app.route('/api/v1.0/temps/<start>/<end>')
def start_end(start, end):
    """Returning min, max, and average temp for this range
        if available, else 404 error message if range unavailable"""

    session = Session(engine)

    lowest2 = session.query(measurement.station, func.min(measurement.tobs).label('min')).filter(measurement.station).all()
    highest2 = session.query(measurement.station, func.max(measurement.tobs).label('max')).filter(measurement.station).all()
    average2 = session.query(measurement.station, func.avg(measurement.tobs).label('avg')).filter(measurement.station).all()

    # close session
    session.close()



    # do I even need this? it was in the example...
    search_terms = start.replace(" ", "").lower()


    for temp in start_end_temps:

    # loop over the sqlite file, and if a date range is 
        if end:
            #find the temps in the range

        elseif:
            #find the temps starting at this date      

    return jsonify(start_end_temps)




if __name__ == '__main__':
    app.run(debug=True)