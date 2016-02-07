import intSender as Packet
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

#!/usr/bin/env python
 
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os


#Create custom HTTPRequestHandler class
class KodeFunHTTPRequestHandler(BaseHTTPRequestHandler):
	#handle GET command
	def do_GET(self):
		rootdir = './html/' #file location
		try:
			print dir(self)
			if self.path.endswith('.html'):
				f = open(rootdir + self.path) #open requested file
		 
				#send code 200 response
				self.send_response(200)
		 
				#send header first
				self.send_header('Content-type','text-html')
				self.end_headers()
		 
				#send file content to client
				self.wfile.write(f.read())
				f.close()
				return
			
		except IOError:
			self.send_error(404, 'file not found')
def run():
	print('http server is starting...')
 
	#ip and port of server
	#by default http server port is 80
	port = 8099;
	server_address = ('127.0.0.1', port)
	httpd = HTTPServer(server_address, KodeFunHTTPRequestHandler)
	print('http server is running... on port: ' + str(port))	
	httpd.serve_forever()
	
if __name__ == '__main__':
	run()

# def main():
	# while(True):
		# message = raw_input('Enter your input:')
		# Packet.sendPacket(0x00, 0x1b, 0x24, 0x07, 0x57, 0x9e, 0x78, 0x24, 0xaf, 0x10, 0x34, 0x44, message);
		# run();
# 
# def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
	# server_address = ('', 8000)
	# httpd = server_class(server_address, handler_class)
	# print "Server oin"
	# httpd.serve_forever()
# 
# 
# 
# if __name__ == "__main__":
	# main()