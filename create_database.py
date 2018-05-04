"""Create schema and generate Sqlite3 Database"""

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Measurement(Base):
    """Hawaii data measurement"""
    __tablename__ = 'measurements'

    id = Column(Integer, primary_key=True)
    station = Column(String)
    date = Column(DateTime)
    prcp = Column(Float)
    tobs = Column(Integer)

def create_database(name):
    filename = f"sqlite:///{name}.sqlite3"
    engine = create_engine(filename, echo=True)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_database("data")
