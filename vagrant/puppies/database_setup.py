from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
	__tablename__ = 'shelter'
	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)
	address = Column(String(250))
	city = Column(String(20))
	state = Column(String(20))
	zipCode = Column(Integer)
	website = Column(String)

class Puppy(Base):
	__tablename__ = 'puppy'
	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)
	dateOfBirth = Column(Date)
	gender = Column(String(6), nullable = False)
	picture = Column(String)
	weight = Column(Numeric(10))
	shelter_id = Column(Integer, ForeignKey('shelter.id'))
	shelter = relationship(Shelter)

#####insert at end of file#######
engine = create_engine('sqlite:///puppies.db')
Base.metadata.create_all(engine)