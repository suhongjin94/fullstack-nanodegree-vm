from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/')
def restaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('index.html', restaurants = restaurants)

@app.route('/restaurants/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return render_template('menuitem.html', items = items, restaurant = restaurant)

@app.route('/restaurants/new/', methods=['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		if (len(request.form['name']) > 0):
			newRest = Restaurant(name=request.form['name'])
			session.add(newRest)
			session.commit()
			flash('Restaurant Succesfully Added')
			return redirect(url_for('restaurants'))		
	else:
		return render_template('newrestaurant.html')

@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
	if request.method == 'POST':
		if (len(request.form['name']) > 0):
			restaurant.name = request.form['name']
			session.add(restaurant)
			session.commit()
			flash('Restaurant Succesfully Edited')
		return redirect(url_for('restaurants'))
	else:
		return render_template('editrestaurant.html', restaurant = restaurant)

@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
	if request.method == 'POST':
		session.delete(restaurant)
		session.commit()
		flash('Restaurant Succesfully Deleted')
		return redirect(url_for('restaurants'))
	else:
		return render_template('deleterestaurant.html', restaurant = restaurant)

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
	if request.method == 'POST':
		name = request.form['name']
		price = request.form['price']
		description = request.form['description']
		course = request.form['course']
		if (len(name) != 0 and len(price) != 0 and len(description) != 0 and len(course) != 0):			
			menuItem = MenuItem(name = name, price = price, description = description, course = course, restaurant = restaurant)
			session.add(menuItem)
			session.commit()
			flash('Menu Item Succesfully Added')
			return redirect(url_for('restaurantMenu', restaurant_id = restaurant.id))
	return render_template('newmenuitem.html', restaurant = restaurant)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
	item = session.query(MenuItem).filter_by(id = menu_id).first()
	if request.method == 'POST':
		if (len(request.form['name']) > 0):
			item.name = request.form['name']
		if (len(request.form['price']) > 0):
			item.price = request.form['price']
		if (len(request.form['description']) > 0):
			item.description = request.form['description']
		session.add(item)
		session.commit()
		flash('Menu Item Succesfully Edited')
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('editmenuitem.html', item = item, restaurant = restaurant)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
	item = session.query(MenuItem).filter_by(id = menu_id).first()
	if request.method == 'POST':
		session.delete(item)
		session.commit()
		flash('Menu Item Succesfully Deleted')
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('deletemenuitem.html', item = item, restaurant = restaurant)


###API ENDPOINTS###
@app.route('/restaurants/JSON/')
def restaurantJSON():
	restaurants = session.query(Restaurant).all()
	return jsonify(Restaurants = [restaurant.serialize for restaurant in restaurants])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return jsonify(MenuItems = [item.serialize for item in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).first()
	if (item != None):
		return jsonify(MenuItem = item.serialize)
	else:
		return "No match found"

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port = 5000)