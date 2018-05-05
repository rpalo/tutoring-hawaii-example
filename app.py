
from datetime import date

from flask import Flask, jsonify, render_template
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

factory = sessionmaker(bind=engine)
Session = scoped_session(factory)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api/v1.0/stations", methods=["GET"])
def get_stations():
    session = Session()
    query = session.query(Station.station)
    result = [record[0] for record in query.all()]
    Session.remove()
    return jsonify(result)

@app.route("/api/v1.0/precipitation", methods=["GET"])
def get_precipitation():
    session = Session()
    query = session.query(Measurement.date, Measurement.prcp).\
                    filter(Measurement.date >= one_year_ago())
    data = {day.isoformat(): prcp for (day, prcp) in query.all()}
    Session.remove()
    return jsonify(data)

@app.route("/api/v1.0/tobs", methods=["GET"])
def get_tobs():
    session = Session()
    query = session.query(Measurement.date, Measurement.tobs).\
                    filter(Measurement.date >= one_year_ago())
    data = {day.isoformat(): tobs for (day, tobs) in query.all()}
    Session.remove()
    return jsonify(data)

@app.route("/api/v1.0/<start>", methods=["GET"])
@app.route("/api/v1.0/<start>/<end>", methods=["GET"])
def get_tobs_range(start, end=None):
    session = Session()
    query = session.query(Measurement.tobs).\
                    filter(Measurement.date >= start)
    if end:
        query = query.filter(Measurement.date <= end)
    temps = pd.DataFrame(query.all())
    Session.remove()
    lo, mid, hi = temps.tobs.min(), temps.tobs.mean(), temps.tobs.max()
    return jsonify({"min": float(lo), "mean": float(mid), "max": float(hi)})


def one_year_ago():
    today = date.today()
    return date(today.year - 1, today.month, today.day)


if __name__ == "__main__":
    app.run(debug=True)