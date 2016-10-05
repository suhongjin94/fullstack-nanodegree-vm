from flask import Flask

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')			
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).first()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
	s = ""
	for item in items:
		s += "%s </br> %s </br> %s </br> </br>" % (item.name, item.price, item.description)
	return s

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)