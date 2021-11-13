# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from scrapeAZCareCheckProject.models import Name, Survey, Enforcement, db_connect, create_table
from scrapeAZCareCheckProject.models_count_facilities import NameCount,db_connect_check, create_table_check
from scrapeAZCareCheckProject.items import ScrapeazcarecheckprojectItem, Scrapeazcarecheckproject_enforcement_Item, Count_Facilities_Item
import logging

class ScrapeazcarecheckprojectPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):

        """Save quotes in the database
        This method is called for every item pipeline component
        """

        if item['name'] == 'GRACE LIVING CARE':

            with open('grace_file_Item.csv', mode='w') as employee_file:
                employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                array1 = []
                array1.append(name)
                employee_writer.writerow(array)

        if item['name'] == 'ACUNA AT MORNING SUN II':

            with open('Acuna_file_Item.csv', mode='w') as employee_file:
                employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                array = []
                array.append(name)
                employee_writer.writerow(array)

        if isinstance(item, ScrapeazcarecheckprojectItem):
            session = self.Session()
            survey = Survey()

            exist_name = session.query(Name).filter_by(facility_name = item['name']).first()
            p = session.query(Name).filter_by(address = item['address']).first()

            if not(p):
                p = Name()
                p.facility_name = item['name']
                p.address = item['address']
                p.city_state = item['city_state']
                p.facility_type = item['facility_type']
                session.add(p)
            p.surveys.append(Survey(address= item['address'], survey_date=item["survey_date"], survey_description=item['survey_description']))
            try:
                session.add(p)

                session.commit()


            except:
                session.rollback()
                raise

            finally:
                session.close()

        return item

class Scrapeazcarecheckproject_enforcement_ItemPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):

        """Save quotes in the database
        This method is called for every item pipeline component
        """
        if isinstance(item, Scrapeazcarecheckproject_enforcement_Item):
            session = self.Session()
            enforcement = Enforcement()

            exist_name = session.query(Name).filter_by(facility_name = item['name']).first()
            p = session.query(Name).filter_by(address = item['address']).first()

            if not(p):
                p = Name()
                p.facility_name = item['name']
                p.address = item['address']
                p.city_state = item['city_state']
                p.facility_type = item['facility_type']
                session.add(p)
            p.enforcements.append(Enforcement(address= item['address'], enforcement_date=item["enforcement_date"], enforcement_description=item['enforcement_description'], name_from_page=item['name_from_page'],facility_name=item['name'],
                                              license=item['license'] ,civil_penalty=item['civil_penalty'],address_from_page=item['address_from_page']))
            try:
                session.add(p)

                session.commit()


            except:
                session.rollback()
                raise

            finally:
                session.close()

        return item


class Count_Facilities_Pipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect_check()
        create_table_check(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):

        """Save quotes in the database
        This method is called for every item pipeline component
        """
        if isinstance(item, Count_Facilities_Item):
            session = self.Session()
            p = NameCount()
            p.facility_name = item['name']
            p.address = item['address']
            p.city_state = item['city_state']
            p.facility_type = item['facility_type']

            try:
                session.add(p)

                session.commit()


            except:
                session.rollback()
                raise

            finally:
                session.close()

        return item
