# Honolulu Climate Analysis

## Overview
`This project involves a detailed climate analysis of Honolulu, Hawaii, using Python, SQLAlchemy, Pandas, Matplotlib, and Flask. It is split into two main parts: analyzing and exploring climate data, and designing a Flask API based on the analysis.`

## Getting Started
### Prerequisites
- Python
- SQLAlchemy
- Pandas
- Matplotlib
- Flask


### Installation
`First, download the necessary files to start your project:`

`Starter Code and Data`

### Files
- climate_starter.ipynb - Jupyter notebook containing the analysis.
- hawaii.sqlite - SQLite database with climate data.

## Part 1: Climate Data Analysis and Exploration
### Steps
1. Database Setup
- Use SQLAlchemy create_engine() to connect to the SQLite database.
- Reflect tables into classes using automap_base().
- Create a session link to the database.

2. Precipitation Analysis
- Find the most recent date in the dataset.
- Retrieve the last 12 months of precipitation data.
- Select "date" and "prcp" values and load them into a DataFrame.
- Sort the DataFrame by "date".
- Plot the results and print summary statistics.

3. Session Closure
- Important: Close your session at the end of your notebook.


## Part 2: Designing the Climate App
### Steps
`Develop a Flask API with the following routes:`

1. Home Page (/)
- List all available routes.

2. Precipitation Data (/api/v1.0/precipitation)
- Return JSON representation of a dictionary with date and prcp values.

3. Station List (/api/v1.0/stations)
- Return a JSON list of stations.

4. Temperature Observations (/api/v1.0/tobs)
- Return a JSON list of temperature observations for the last year from the most-active station.

5. Temperature Stats (/api/v1.0/<start> and /api/v1.0/<start>/<end>)
- Return a JSON list of TMIN, TAVG, and TMAX for a given date range.

## Conclusion
`This project is a comprehensive approach to understanding the climate trends in Honolulu. Following these steps will lead to insightful data visualizations and an interactive API for exploring the climate data.`