import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, timedelta

from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///../Resources/hawaii.sqlite", echo=False)


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

# Create the app an pass __name__
app = Flask(__name__)

# Define the the routes and list them on the index page
@app.route('/')
def home():
    print('Welcome to My Page')      #The Print result will not show on the client side
    html = """
    <h1> Welcome to My Climate App </h1>
    <a href="/api/v1.0/precipitation">Precipitation Analysis</a>
    <br>
    <a href="/api/v1.0/stations">Station Analysis</a>
    <br>
    <a href="/api/v1.0/tobs">Temperature Observation of Most Active Station</a>
    <br>
    """
    return html

@app.route('/api/v1.0/precipitation')
def precipitation():
    # Create a session link from Python to the DB
    session = Session(engine)
    print('This is the Precipitation Page')
    
    # Query all date and precipitation scores, starting from the most recent data point
    most_recent_date = session.query(func.max(Measurement.date))
    most_recent_date_pt = most_recent_date.scalar()
    most_recent_date_object = datetime.strptime(most_recent_date_pt, "%Y-%m-%d")
    
    # Calculate the date one year from the last date in data set.
    date_twelve_mos_ago = most_recent_date_object - timedelta(days=365)
    
    # # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp)\
                     .filter(Measurement.date >= date_twelve_mos_ago)\
                     .order_by(most_recent_date).all()

    # Close the session
    session.close()
    
    # Create a dictionary from the above query and append to a list
    precipitation_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        precipitation_data.append(prcp_dict)
        
    # Jsonify the dictionary
    return jsonify(precipitation_data)

@app.route('/api/v1.0/stations')
def stations():
    print('This is the Station Page')
    return f'Station Page'   


@app.route('/api/v1.0/tobs')
def tobs():
    print('This is the Temperature Observed Page')
    return f'Temperature Observed Page'


if __name__ == '__main__':
    app.run(debug=True)