# Import files from first lesson. Used for connections to the DB #
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from restaurants import Base, Restaurant, MenuItem

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# Create session and connect to the DB #
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		output = ""
		output += "<html lang = ""en"">"
		output += '''<head>
		    				<script src=""https://code.jquery.com/jquery-3.0.0.min.js""></script>
		    			</head>'''
		output += "<body>"
		try:
			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output += "<a href = '/restaurants/new' >Make a New Restaurant Here</a><BR>"
				restaurants = session.query(Restaurant)\
					.order_by(Restaurant.name).all()

				for restaurant in restaurants:
					output += "<p>" + restaurant.name + "<BR>"
					output += "<a href='/restaurants/%s/edit' >Edit</a>" % restaurant.id
					output += "<BR>"
					output += "<a href='/restaurants/%s/delete' >Delete</a>" % restaurant.id
					output += "</p>"

				output += "</body></html>"

				self.wfile.write(output)
				#print output
				return

			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output += "<h1>Make a New Restaurant</h1>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
				output += "<input name='newRestaurantName' type='text' placeholder='New Restaurant Name'>"
				output += "<input type='submit' value='Create'> </form>"
				output += "</body></html>"

				self.wfile.write(output)
				#print output
				return

			if self.path.endswith("/edit"):
				restaurantIDPath = self.path.split("/")[2]
				myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
				if myRestaurantQuery:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output += "<h1>" + myRestaurantQuery.name + "</h1>"
					output += "<form method='POST' enctype='multipart/form-data' action='restaurants/%s/edit'>" % restaurantIDPath
					output += '<input name = "newRestaurantName" type ="text" placeholder = "%s" >' % myRestaurantQuery.name
					output += "<input type='submit' value='Rename'>"
					output += "</form>"
					output += "</body></html>"

					self.wfile.write(output)
					#print output
					return

			if self.path.endswith("/delete"):
				restaurantIDPath = self.path.split("/")[2]
				myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
				if myRestaurantQuery:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output += "<h1>Are you sure you want to delete " + myRestaurantQuery.name + "?</h1>"
					output += "<form method='POST' enctype='multipart/form-data' action='restaurants/%s/delete'>" % restaurantIDPath
					output += "<input name = 'deleteRestaurantID' type= 'hidden' value= %s>" % myRestaurantQuery.id
					output += "<input type='submit' value='Delete'>"
					output += "</form>"
					output += "</body></html>"

					self.wfile.write(output)
					#print output
					return

		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)

	def do_POST(self):
		try:
			if self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newRestaurantName')
					restaurantIDPath = self.path.split("/")[2]

					myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
					if myRestaurantQuery:
						myRestaurantQuery.name = messagecontent[0]
						session.add(myRestaurantQuery)
						session.commit()
						self.send_response(301)
						self.send_header('Content-type', 'text/html')
						self.send_header('Location', '/restaurants')
						self.end_headers()

			if self.path.endswith("/delete"):
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('deleteRestaurantID')
					restaurantIDPath = self.path.split("/")[2]

					myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
					if myRestaurantQuery:
						myRestaurantQuery.id = messagecontent[0]
						session.delete(myRestaurantQuery)
						session.commit()
						self.send_response(301)
						self.send_header('Content-type', 'text/html')
						self.send_header('Location', '/restaurants')
						self.end_headers()

			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newRestaurantName')

					# Create new Restaurant class
					newRestaurant = Restaurant(name=messagecontent[0])
					session.add(newRestaurant)
					session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()

		except:
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
