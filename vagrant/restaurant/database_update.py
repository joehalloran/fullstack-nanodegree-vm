from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

## Database connection
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

## Find item to update
veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')

## Output filtered query 
for burger in veggieBurgers:
	print(burger.id)
	print(burger.price)
	print(burger.restaurant.name)
	print("\n")

## Filter by id to find one item
singleVeggieBurger = session.query(MenuItem).filter_by(id = 10).one()

## Update single item
singleVeggieBurger.price = '$2.99'

# Add and commit update
session.add(singleVeggieBurger)
session.commit()

# Change price of all burgers
for burger in veggieBurgers:
	if burger.price != '$2,99':
		burger.price = '$2.99'
		session.add(burger)
		session.commit()