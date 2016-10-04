#database imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

#webserver imports
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

'''
Objective of this webserver
1) Show list of restaurants in database
2) Show links for edit & delete
3) Allow creation of restaurants
4) Allow updating name of restaurants
5) Allow deletion of restaurants
'''

#Connect to database
engine = create_engine('sqlite:///restaurantmenu.db')			
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body><h1>List of restaurants</h1>"
				restaurants = session.query(Restaurant).all()
				for restaurant in restaurants:
					output += "<h2>" + restaurant.name + "</h2>"
					output += "<a href='/restaurants/" + str(restaurant.id) + "/edit'>Edit</a></br>"
					output += "<a href='/restaurant/" + str(restaurant.id) + "/delete'>Delete</a>"
				output += "<h2><a href='/restaurants/new'>Create new restaurant</a><h2>"
				output += "</body></html>"
				self.wfile.write(output)

			elif self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body><h1>Create new restaurant</h1>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Name of new restaurant</h2><input name='restaurant_name' type='text' ><input type= 'submit' value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)

			elif self.path.endswith("/edit"):
				restaurantId = self.path.split("/")[2]
				restaurant = session.query(Restaurant).filter_by(id = restaurantId).first()
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body><h1>Edit restaurant: %s</h1>" % restaurant.name
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/" + str(restaurantId) + "/edit'><h2>Update</h2><input name='restaurant_name' type='text' ><input type= 'submit' value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)

			elif self.path.endswith("/delete"):
				restaurantId = self.path.split("/")[2]
				restaurant = session.query(Restaurant).filter_by(id = restaurantId).first()
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body><h1>Delete restaurant: %s?</h1>" % restaurant.name
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/" + str(restaurantId) + "/delete'><input type= 'submit' name='delete' value='Delete'> <input type= 'submit' name='cancel' value='Cancel'></form>"
				output += "</body></html>"
				self.wfile.write(output)


		except IOError:
			self.send_error(404, "File not found %s" % self.path)

	def do_POST(self):
		try:
			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype =='multipart/form-data': #check if form data
					fields=cgi.parse_multipart(self.rfile, pdict) #collect all data
					messagecontent = fields.get('restaurant_name') #get specific
					restaurant = Restaurant(name=messagecontent[0])
					session.add(restaurant)
					session.commit()
					self.send_response(301)
					#redirect
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()

			elif self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype =='multipart/form-data': #check if form data
					fields=cgi.parse_multipart(self.rfile, pdict) #collect all data
					messagecontent = fields.get('restaurant_name') #get specific
					restaurantId = self.path.split("/")[2]
					restaurant = session.query(Restaurant).filter_by(id = restaurantId).first()
					restaurant.name = messagecontent[0]
					session.add(restaurant)
					session.commit()
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()

			elif self.path.endswith("/delete"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype =='multipart/form-data': #check if form data
					fields=cgi.parse_multipart(self.rfile, pdict) #collect all data
					messagecontent = fields.get('delete') #get specific
					if messagecontent != None:
						restaurantId = self.path.split("/")[2]
						restaurant = session.query(Restaurant).filter_by(id = restaurantId).first()
						session.delete(restaurant)
						session.commit()
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()


		except:
			print 'EXCEPTION'
			pass


def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()

	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()

if __name__ == '__main__':
	main()