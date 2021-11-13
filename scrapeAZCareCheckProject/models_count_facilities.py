from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text)
from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect_check():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table_check(engine):
    Base.metadata.create_all(engine)


# Association Table for One-To-Many relationship between Quote and Tag
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
class NameCount(Base):
    __tablename__ = 'name_count'
    id = Column(Integer, primary_key=True)
    facility_name = Column('facility_name', String(50), unique=False)

    address = Column('address', String(50), unique=False)
    city_state = Column('city_state', String(50), unique=False)
    facility_type = Column('facility_type', String(50), unique=False)
