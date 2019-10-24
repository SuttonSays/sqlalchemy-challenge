import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt
from DateTime import DateTime

# Dictionary of Justice League
justice_league_members = [
    {"superhero": "Aquaman", "real_name": "Arthur Curry"},
    {"superhero": "Batman", "real_name": "Bruce Wayne"},
    {"superhero": "Cyborg", "real_name": "Victor Stone"},
    {"superhero": "Flash", "real_name": "Barry Allen"},
    {"superhero": "Green Lantern", "real_name": "Hal Jordan"},
    {"superhero": "Superman", "real_name": "Clark Kent/Kal-El"},
    {"superhero": "Wonder Woman", "real_name": "Princess Diana"}
]

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the json representation of the dictionary"""

# Design a query to retrieve the last 12 months of precipitation data and plot the results
# Calculate the date 1 year ago from the last data point in the database

# Latest Date
latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
latest_date

 # Date 12 months from the latest date
last_twelve_months = dt.datetime.strptime(latest_date, '%Y-%m-%d') - dt.timedelta(days=365)
last_twelve_months

 # Retrieve the last 12 months of precipitation data
rain_results = session.query(Measurement.date, func.avg(Measurement.prcp)).\
                    filter(Measurement.date >= last_twelve_months).\
                    group_by(Measurement.date).all()
rain_results

# Save the query results as a Pandas DataFrame and set the index to the date column, and sort by date
rain_df = pd.DataFrame(rain_results, columns=['Date', 'Precipitation'])
rain_df.set_index('Date', inplace=True)
rain_df.head()

rain_df = rain_df.sort_values(by = 'Date')
rain_df.head()

rain_df_dic = rain_df.to_dict()


    return jsonify(rain_df_dic)


@app.route("/api/v1.0/stations")
def stations():
    """Return the json list of stations from the dataset
    # List the stations and the counts in descending order."""

    # Design a query to show how many stations are available in this dataset?
    session.query(Station.id).count()

    rain_results = session.query(Measurement.station, func.count(Measurement.station)).\
            group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).all()
    rain_results

    rain_df = pd.DataFrame(rain_results, columns=['Date', 'Precipitation'])
    rain_df.set_index('Date', inplace=True)
    rain_df.head()

    rain_results_dic = rain_results.to_dict()

    # Using the station id from the previous query, calculate the lowest temperature recorded, 
    # highest temperature recorded, and average temperature of the most active station?
    # Data displays as Lowest, Average,Highest)
   
    awesome_station = rain_results[0][0]
    session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.station == awesome_station).all()

    return jsonify(rain_results_dic) 


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of tempereature observations for the prior year"""
    temp_results = session.query(Measurement.station, Measurement.tobs).\
                filter(Measurement.station == awesome_station).\
                filter(Measurement.date >= last_twelve_months).all()
    tempobserv_df = pd.DataFrame(temp_results)
    tempobserv_df.set_index('station', inplace=True)
    tempobserv_df.head()

    return jsonify(tempobserv_df)

@app.route("/api/v1.0/<start>")
def start():
    """Return a JSON list of the minimum temperature, the average temperature,
    And the max emperature for a given start or start-end range"""

    return jsonify(justice_league_members)
@app.route("/api/v1.0/<start>/<end>")
def start/end():
    """When given only the start, calculate TMIN, TAVG and TMAX for all dates greater than or equal to the start date"""
    """When the given start and the dnd date, calculate the TMIN, TAVG, and TMAX for the dates between the start and inclusive.
    return jsonify(justice_league_members)



if __name__ == "__main__":
    app.run(debug=True)
