import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)

@app.route('/')
def home():
    output = ('<h2>To see the data go to the following routes:</h2>' +
    '<ul>' +
    '<li>/api/v1.0/precipitation</li>' +
    '<li>/api/v1.0/stations</li>' +
    '<li>/api/v1.0/tobs</li>' +
    '<li>/api/v1.0/<start> and /api/v1.0/<start>/<end></li>' +
    '</ul>')

    return output

@app.route('/api/v1.0/precipitation')
def prcp():
    session = Session(engine)
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date > '2016-08-23').all()
    session.close()
    return { date:prcp for date,prcp in results }

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    results = session.query(station.station, station.name).filter(measurement.date > '2016-08-23').all()
    session.close()
    return { date:prcp for date,prcp in results }

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    results = session.query(measurement.date, measurement.tobs).filter((measurement.date > '2016-08-23')&(measurement.station=='USC00519281')).all()
    session.close()
    return { date:tobs for date,tobs in results }

@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def agg(start,end='2017-08-23'):
    session = Session(engine)
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs),func.max(measurement.tobs)).filter((measurement.date >= start)&(measurement.date <= end)).all()
    return jsonify(results)



if __name__=="__main__":
    app.run(debug=True)

