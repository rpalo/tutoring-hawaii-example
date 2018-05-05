"""Create schema and generate Sqlite3 Database"""

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine("sqlite:///hawaii.sqlite", echo=True)

class Measurement(Base):
    """Hawaii data measurement"""
    __tablename__ = 'measurement'

    measurement_id = Column(Integer, primary_key=True)
    station = Column(String)
    date = Column(Date)
    prcp = Column(Float)
    tobs = Column(Integer)

class Station(Base):
    """Hawaii weather stations"""
    __tablename__ = 'station'

    station_id = Column(Integer, primary_key=True)
    station = Column(String)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)

def create_database():
    Base.metadata.create_all(engine)

def load_data():
    measurements = pd.read_csv("clean_hawaii_measurements.csv")
    stations = pd.read_csv("hawaii_stations.csv")
    measurements.to_sql('measurement', engine, if_exists='append', index=False)
    stations.to_sql('station', engine, if_exists='append', index_label='station_id')

if __name__ == "__main__":
    create_database()
    load_data()