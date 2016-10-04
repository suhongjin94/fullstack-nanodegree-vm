from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

entries = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for entry in entries:
	if entry.price != '$2.99':
		entry.price = '$2.99'
		session.add(entry)
		session.commit()
# urbanBurger = session.query(MenuItem).filter_by(id = 1).one()
# urbanBurger.price = '$2.99'
# session.add(urbanBurger)
# session.commit()
for entry in entries:
	print entry.price