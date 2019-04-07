#
# Title:sql_table.py
# Description: SQLAlchemy adapter
# Development Environment:OS X 10.9.3/Python 2.7.7
# Author:G.S. Cole (guycole at gmail dot com)
#
from sqlalchemy import Column
from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, String

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    month = Column(Integer)
    day = Column(Integer)
    year = Column(Integer)
    date = Column(Date)
    note = Column(String)

    def __init__(self, month, day, year, date, note):
        self.month = month
        self.day = day
        self.year = year
        self.date = date
        self.note = note

    def __repr__(self):
        return "<event(%d %d %d %s %s)>" % (self.id, self.month, self.day, self.date, self.note)