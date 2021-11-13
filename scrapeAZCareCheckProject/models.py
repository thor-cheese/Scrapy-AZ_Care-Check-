from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text)
from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


# Association Table for One-To-Many relationship between Quote and Tag
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
class Name(Base):
    __tablename__ = 'name'
    id = Column(Integer, primary_key=True)
    facility_name = Column('facility_name', String(50), unique=False)

    address = Column('address', String(50), unique=False)
    city_state = Column('city_state', String(50), unique=False)
    facility_type = Column('facility_type', String(50), unique=False)
    surveys = relationship('Survey', backref='name')  # One name to many surveys
    enforcements = relationship('Enforcement', backref='name')  # One name to many surveys


class Survey(Base):
    __tablename__ = 'survey'
    id = Column(Integer, primary_key=True)
    name_id = Column(Integer, ForeignKey('name.id'))
    address = Column('address', String(50), unique=False)
    survey_date = Column('survey_date', String(50), unique=False)
    survey_description = Column('survey_description', String(50), unique=False)

class Enforcement(Base):
    __tablename__ = 'enforcement'
    id = Column(Integer, primary_key=True)
    name_id = Column(Integer, ForeignKey('name.id'))
    name_from_page = Column('name_from_page', String(50), unique=False)
    facility_name = Column('facility_name', String(50), unique=False)
    address_from_page = Column('address_from_page', String(50), unique=False)
    address = Column('address', String(50), unique=False)
    license = Column('license', String(50), unique=False)
    enforcement_date = Column('enforcement_date', String(50), unique=False)
    civil_penalty = Column('civil_penalty', String(50), unique=False)
    enforcement_description = Column('enforcement_description', String(50), unique=False)
