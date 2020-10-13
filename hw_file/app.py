
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
Passenger = Base.classes.passenger

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Do not need this function for this exercise...
# def double(inp):
#     if inp is not None:
#         return inp*2
#     else:
#         return None

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    # Convert query results to a dict using date as the key and prcp as the value
    session = Session(engine)
    results = session.query(Passenger.name).all()

    # close the session to end communication with the server
    session.close()

    all_locs_prep = list(np.ravel(results))
    # alternative with list comprehension
    # all_names = [result[0] for result in results]

    return jsonify(all_locs_prep)


@app.route('/api/v1.0/stations')
def stations():

    # Return a JSON list of stations from the dataset 


    ############### Database Block ###################
    # Start session
    session = Session(engine)

    # Query the database
    results = session.query(stations).all()

    # close session
    session.close()
    ###################################################

    ################### Processing ####################
    all_stations = []
    for stations in results:
        passenger_dict = {}
        passenger_dict['name'] = {'first':passenger.name.split(' ')[1],'last':passenger.name.split(' ')[0]}
        passenger_dict['age'] = passenger.age
        passenger_dict['doubleAge'] = double(passenger.age)
        passenger_dict['sex'] = passenger.sex
        all_passengers.append(passenger_dict)
    ####################################################

    return jsonify(all_stations)


@app.route('/api/v1.0/tobs')
def tobs():

    return (
        some stuff....
    )

@app.route('/api/v1.0/start')
def start():

    return (
        some stuff....
    )


@app.route('/api/v1.0/start/end')
def start_end():

    return (
        some stuff....
    )




if __name__ == '__main__':
    app.run(debug=True)