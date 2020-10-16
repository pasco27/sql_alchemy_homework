
## This is a flast app for the SQLAlchemy HW
## Using the titanic app class example as a base document


import numpy as np
import os

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
    # List all available api routes
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
    for row in precip:
        measurements = {}
    
       # i had this below, tutor pointed out that the directtions stated that the 'date' should be the KEY
       # that makes sense to me, but the below code is cleaner -- keeping it per directions as 'date'= KEY
       # measurement['date'] = measurement.date
       # measurement['precipitaion'] = measurement.prcp
       # hawaii_measurements.append(measurements)   
    
        measurements[row.date]= row.prcp
        hawaii_measurements.append(measurements) 

    return jsonify(hawaii_measurements)

    # all_locs_prcp = list(np.ravel(results))
    # alternative with list comprehension
    # all_names = [result[0] for result in results]


@app.route('/api/v1.0/stations')
def stations():
    # Return a JSON list of stations from the dataset 
    
    # Query the database
    session = Session(engine)
    station_count = session.query(measurement.station).group_by(measurement.station).all()
    # close session
    session.close()

    return jsonify(station_count)



@app.route('/api/v1.0/tobs')
def tobs():
    # Query the dates and temperature observations of the most active station for the last year of data.
    # for simplicity of the exercise I know from the precip analysis portion that most active == USC00519281 
    
    # Query the database
    session = Session(engine)
    dates_and_temps = session.query(measurement.date, measurement.prcp).filter(measurement.station == 'USC00519281').filter(measurement.date >= "2016-08-23").all()

    #These were from MIN, and latest year ... from jupyter notebook
    #lowest2 = session.query(measurement.station, func.min(measurement.tobs).label('min')).filter(measurement.station=='USC00519281').all()
    #past_year = session.query(measurement.date, measurement.prcp).filter(measurement.date >= "2016-08-23").all()
    # close session
    session.close()    

    tobs_results = list(np.ravel(dates_and_temps))
    
    return jsonify(dates_and_temps)

###### STARTED this route, but worked with tutor and created the below in which both start/end were created in one route!
# @app.route('/api/v1.0/<start>')
# def start():
#     # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date
    
#     # Query the database
#     session = Session(engine)

#     # close session
#     session.close()
    
#     return jsonifty(xyz)


@app.route('/api/v1.0/temps/<start>')
@app.route('/api/v1.0/temps/<start>/<end>')
def start_end(start = None, end = None):
    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive

    session = Session(engine)

    # loop over the sqlite file, and if a date range is 
    # if end:
    #         #find the temps in the range

    # else:
    #         #find the temps starting at this date 

    if end:

        # SELECT  * FROM... 
        # WHERE

        # copied this code over from my jupyter notebook which helped form the filter below
        # lowest2 = session.query(measurement.station, func.min(measurement.tobs).label('min')).filter(measurement.station).all()
        # highest2 = session.query(measurement.station, func.max(measurement.tobs).label('max')).filter(measurement.station).all()
        # average2 = session.query(measurement.station, func.avg(measurement.tobs).label('avg')).filter(measurement.station).all()

        init_query = session.query(func.min(measurement.tobs).label('min'), func.max(measurement.tobs).label('max'), func.avg(measurement.tobs).label('avg'))
        results_end = init_query.filter(measurement.date >= start).filter(measurement.date <= end).all()

    else:

        init_query = session.query(func.min(measurement.tobs).label('min'), func.max(measurement.tobs).label('max'), func.avg(measurement.tobs).label('avg'))
        results_end = init_query.filter(measurement.date >= start).all()

    # close session
    session.close()



    hawaii_measurements_dates = []
    for row in results_end:
        measurements = {}
    # here, utlizing my orig earlier idea from the Titanic example
        measurements['min temp']= row.min
        measurements['max temp']= row.max
        measurements['average temp']= row.avg
        hawaii_measurements_dates.append(measurements) 

    return jsonify(hawaii_measurements_dates)   



if __name__ == '__main__':
    app.run(debug=True)