from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shelter, Puppy
import datetime

engine = create_engine('sqlite:///puppies.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#helper functions for problems
def isLeapYear(year):
	if year % 4 != 0:
	    return False
	elif year % 100 != 0:
		return True
	elif year % 400 != 0:
		return False
	else:
		return True

def subtract6Months(date):
	timetup = date.timetuple()
	if (isLeapYear(timetup[0]) and timetup[1] > 2):
		subDate = date - datetime.timedelta(days = 182)
	else:
		subDate = date - datetime.timedelta(days = 183)
	return subDate

#1. Query all of the puppies and return the results in ascending alphabetical order
def p1():
	entries = session.query(Puppy).order_by(Puppy.name)
	for entry in entries:	
		print entry.name
		print entry.dateOfBirth

#2. Query all of the puppies that are less than 6 months old organized by the youngest first
def p2():
	today = datetime.date.today()
	earliestDate = subtract6Months(today)
	entries = session.query(Puppy).filter(Puppy.dateOfBirth > earliestDate).order_by(Puppy.dateOfBirth)
	for entry in entries:
		print entry.name
		print entry.dateOfBirth

#3. Query all puppies by ascending weight
def p3():
	entries = session.query(Puppy).order_by(Puppy.weight)
	for entry in entries:
		print entry.name
		print entry.weight

#4. Query all puppies grouped by the shelter in which they are staying
def p4():
	entries = session.query(Puppy).order_by(Puppy.shelter_id).all()
	for entry in entries:
		print entry.name
		print entry.shelter_id

p4()