from flask import Flask

# Import files from first lesson. Used for connections to the DB #
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from restaurants import Base, Restaurant, MenuItem

app = Flask(__name__)

# Create session and connect to the DB #
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/')
def restaurant_list():
	restaurants = session.query(Restaurant).order_by(Restaurant.name).all()
	output = ''
	output += '<h2>List of Restaurants</h2>'
	for restaurant in restaurants:
		output += restaurant.name + ': %s' % restaurant.id + '</br>'

	return output


@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)

	output = ''
	output += '<h2>' + restaurant.name + '</h2>'
	for i in items:
		output += '<p>'
		output += i.name + ': %s' % i.id + '</br>'
		output += i.price + '</br>'
		output += i.description
		output += '</p>'

	return output

# Task 1: Create route for newMenuItem function here


@app.route('/restaurants/<int:restaurant_id>/new/')
def new_menu_item(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

	output = ''
	output += 'page to add a new menu item. Task 1 complete!</br>'
	output += 'The restaurant is: %s' % restaurant.name + '</br>'
	return output

# Task 2: Create route for editMenuItem function here


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/')
def edit_menu_item(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	item = session.query(MenuItem).filter_by(restaurant_id=restaurant.id, id=menu_id).one()

	output = ''
	output += 'page to edit a menu item. Task 2 complete!</br>'
	output += 'The restaurant is: %s' % restaurant.name + '</br>'
	output += 'The menu item to edit is: %s' % item.name + '</br>'
	return output

# Task 3: Create a route for deleteMenuItem function here


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/')
def delete_menu_item(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	item = session.query(MenuItem).filter_by(restaurant_id=restaurant.id, id=menu_id).one()

	output = ''
	output += 'page to delete a menu item. Task 3 complete!</br>'
	output += 'The restaurant is: %s' % restaurant.name + '</br>'
	output += 'The menu item to delete is: %s' % item.name + '</br>'
	return output

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)

