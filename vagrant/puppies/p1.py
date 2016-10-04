'''
1. Query all of the puppies and return the results in ascending alphabetical order
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shelter, Puppy

engine = create_engine('sqlite:///puppies.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

entries = session.query(Puppy).order_by(Puppy.name)
for entry in entries:
	print entry.name
	print entry.dateOfBirth