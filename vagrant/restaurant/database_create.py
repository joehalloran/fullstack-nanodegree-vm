from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

## Database connection
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


## Add to Restaurant table
myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()

## Add to MenuItem table
cheesePizza = MenuItem(name = "Cheese Pizza", description = "Made with all natural ingredients and fresh Mozzarella", course = "Entree", price = "$8.99", restaurant = myFirstRestaurant)
session.add(cheesePizza)
session.commit()
