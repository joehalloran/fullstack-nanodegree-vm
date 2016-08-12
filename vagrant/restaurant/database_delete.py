from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

## Database connection
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

## Find item to delete
spinachIceCream = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
print(spinachIceCream.restaurant.name)

## Delete the item
session.delete(spinachIceCream)
session.commit()
