from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

## Database connection
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

## Read first restaurant
firstResult = session.query(Restaurant).first()
print(firstResult.name, firstResult.id)

## Read all menu items 
items = session.query(MenuItem).all()
for item in items:
	print(item.name, item.description, item.id, item.price)