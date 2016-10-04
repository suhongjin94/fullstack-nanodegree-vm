'''
2. Query all of the puppies that are less than 6 months old organized by the youngest first
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shelter, Puppy
from datetime import datetime

engine = create_engine('sqlite:///puppies.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

earliestDate = datetime.strptime('2016-04-03', '%Y-%m-%d')
entries = session.query(Puppy).filter(Puppy.dateOfBirth > earliestDate).order_by(Puppy.dateOfBirth)
for entry in entries:
	print entry.name
	print entry.dateOfBirth