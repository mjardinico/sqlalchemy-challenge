import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, timedelta

from flask import Flask, jsonify, request, redirect, url_for

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
    <br><br>
    <a href="/api/v1.0/stations">Station Analysis</a>
    <br><br>
    <a href="/api/v1.0/tobs">TOBS of the Most Active Station</a>
    <br><br>
    
    <h2>Temperature Statistics</h2>
    <form action="/api/v1.0/temperature_stats" method="get">
        <label for="start">Start Date:</label>
        <input type="date" id="start" name="start">
        <label for="end">End Date (optional):</label>
        <input type="date" id="end" name="end">
        <input type="submit" value="Get Temperature Stats">
    </form>
    <br>
    """
    return html

@app.route('/api/v1.0/precipitation')
def precipitation():
    # Create a session link from Python to the DB
    session = Session(engine)
    
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
        
    # Return the JSON representation of your dictionary
    return jsonify(precipitation_data)

@app.route('/api/v1.0/stations')
def stations():
    
    # Create a session link from Python to the DB
    session = Session(engine)
            
    # # Design a query to calculate the total number of stations in the dataset
    # station_count = session.query(Station).count()
    
    # Design a query to find the most active stations (i.e. which stations have the most rows?)
    # List the stations and their counts in descending order.
    station_query = session.query(Measurement.station,func.count(Measurement.station).label('count'))\
                    .group_by(Measurement.station).order_by(func.count(Measurement.station).desc())

    # Close the session
    session.close()
    
    # Create a list of stations and their counts
    station_list = [(item.station, item.count) for item in station_query]
    
    # Return a JSON list of stations from the dataset
    return jsonify(station_list)    


@app.route('/api/v1.0/tobs')
def tobs():
    
    # Create a session link from Python to the DB
    session = Session(engine)
    
    # Query all date and precipitation scores, starting from the most recent data point
    most_recent_date = session.query(func.max(Measurement.date))
    most_recent_date_pt = most_recent_date.scalar()
    most_recent_date_object = datetime.strptime(most_recent_date_pt, "%Y-%m-%d")
    
    # Calculate the date one year from the last date in data set.
    date_twelve_mos_ago = most_recent_date_object - timedelta(days=365)
    
    # Design a query to find the most active stations (i.e. which stations have the most rows?)
    # List the stations and their counts in descending order.
    station_query = session.query(Measurement.station,func.count(Measurement.station).label('count'))\
                .group_by(Measurement.station).order_by(func.count(Measurement.station).desc())

    # Close the session
    session.close()
    
    
    # Extract them most active station from station_query using the .first() method.
    most_active_station = station_query.first()
    most_active_station_id = most_active_station[0]    
        
    # Using the most active station id
    # Query the last 12 months of temperature observation data (tobs) for station most_active_station_id
    # tobs_query = session.query(Measurement.tobs).filter(Measurement.station == most_active_station_id, Measurement.date > date_twelve_mos_ago)
    tobs_query = session.query(Measurement.tobs, Measurement.date).filter(Measurement.date > date_twelve_mos_ago)

    # Create a list of stations and their counts
    tobs_list = [(item.date, item.tobs) for item in tobs_query]
    
    # Return a JSON list of temperature observations for each date from the previous year
    return jsonify(tobs_list)

# Let's create a route to handle the form submission from the index page
@app.route('/api/v1.0/temperature_stats')
def temperature_stats():
    start = request.args.get('start')
    end = request.args.get('end')

    if not start:
        # Handle the case where start date is not provided
        return "Start date is required.", 400

    if end:
        return redirect(url_for('temp_stats', start=start, end=end))
    else:
        return redirect(url_for('temp_stats', start=start))


@app.route('/api/v1.0/<start>')        #makes the end date as optional on this line
@app.route('/api/v1.0/<start>/<end>')
def temp_stats(start, end=None):
    # Create a session link from Python to the DB
    session = Session(engine)
    
    # Convert start (and optional end date) strings to datetime object
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d") if end else None
    
    # Perform a query to retrieve the temperature statistics 
    if end_date:
        results = session.query(func.min(Measurement.tobs),
                                func.avg(Measurement.tobs),
                                func.max(Measurement.tobs))\
                          .filter(Measurement.date >=start_date)\
                          .filter(Measurement.date <= end_date).all() 
    else:
        results = session.query(func.min(Measurement.tobs),
                                func.avg(Measurement.tobs),
                                func.max(Measurement.tobs))\
                          .filter(Measurement.date >=start_date).all()
    session.close()
    
    
    # Unpack the query result
    tmin, tavg, tmax = results[0]
    
    # Format the data to be returned as JSON
    temp_stats_data = {
        'Start Date': start,
        'End Date': end if end else 'Present',
        'Min Temperature': tmin,
        'Average Temperature': tavg,
        'Max Temperature': tmax       
    }
    
    return jsonify(temp_stats_data)

if __name__ == '__main__':
    app.run(debug=True)
    
# END OF CODE