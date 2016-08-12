from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# Database dependencies
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Database connection
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
	
	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>Hello!"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"
				output += "</body></html>"

				self.wfile.write(output)
				print(output)
				return

			if self.path.endswith("/restaurants"):
				restaurants = session.query(Restaurant).all()
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<a href='/restaurants/new'>Create a new restaurant</a>"
				output += "<h1>Restaurants</h1>"
				for restaurant in restaurants:
					output += restaurant.name
					output += "<br />"
					output += "<a href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
					output += "<br />"
					output += "<a href='/restaurants/%s/delete'>Delete</a>" % restaurant.id
					output += "<br /><br /><br />"
				output += "</body></html>"

				self.wfile.write(output)
				print(output)
				return
			
			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1>New Restaurant</h1>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
				output += "<input name='newRestaurantName' type='text' >"
				output += "<input type='submit' value='Submit'></form>"
				output += "</body></html>"

				self.wfile.write(output)
				print(output)
				return

			if self.path.endswith("/edit"):
				restaurantIDPath = self.path.split("/")[2]

				restaurant = session.query(Restaurant).filter_by(id = restaurantIDPath).one()

				if restaurant:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					
					output = ""
					output += "<html><body>"
					output += "<h1>Rename Restaurant</h1>"
					output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurantIDPath
					output += "<input name='editRestaurantName' type='text' placeholder='%s' >" % restaurant.name
					output += "<input type='submit' value='Submit'></form>"
					output += "</body></html>"

					self.wfile.write(output)
					print(output)
					return

			if self.path.endswith("/delete"):
				restaurantIDPath = self.path.split("/")[2]

				restaurant = session.query(Restaurant).filter_by(id = restaurantIDPath).one()

				if restaurant:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					
					output = ""
					output += "<html><body>"
					output += "<h1>Are you sure you want to delete %s</h1>" %restaurant.name
					output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurantIDPath
					output += "<input type='submit' value='Delete'></form>"
					output += "</body></html>"

					self.wfile.write(output)
					print(output)
					return

		except IOError:
			print("Error")
			self.send_error(404, "File Not Found %s" % self.path)

	def do_POST(self):
		try:
			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messageContent = fields.get('newRestaurantName')

				## Add to Restaurant table
				newRestaurant = Restaurant(name = messageContent[0])
				session.add(newRestaurant)
				session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()

				return

			if self.path.endswith("/edit"):
				restaurantIDPath = self.path.split("/")[2]

				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messageContent = fields.get('editRestaurantName')

				## Update Restaurant name
				updateRestaurant = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
				if updateRestaurant:
					updateRestaurant.name = messageContent[0]
					session.add(updateRestaurant)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()

				return

			if self.path.endswith("/delete"):
				restaurantIDPath = self.path.split("/")[2]

				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

				## Update Restaurant name
				deleteRestaurant = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
				
				if deleteRestaurant:
					session.delete(deleteRestaurant)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()

				return


			"""
			self.send_response(301)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				fields = cgi.parse_multipart(self.rfile, pdict)
				messageContent = fields.get('newRestaurantName')


			output = ""
			output += "<html><body>"
			output += "<h2>Okay, how about this:</h2>"
			output += "<h1> %s </h1>" % messageContent[0]
			output += "</body></html>"

			self.wfile.write(output)
			print(output)
			"""

		except:
			pass
	

def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print "Web server running in port %s" % port
		server.serve_forever()



	except KeyboardInterrupt:
		print("Ctrl+C entered, stopping webserver ...")
		server.socket.close()

if __name__ == '__main__':
	main()