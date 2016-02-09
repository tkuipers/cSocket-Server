from flask import Flask
from flask import request
import sendSocket as Packet
import threading
app = Flask(__name__)
app._static_folder = "/home/tyler/Documents/SmartHome/cSocket-Server/"

def startListener():
	while True:
		try:
			mac = Packet.listen("\xFF\xFF\xFF\xFF\xFF\xFF", "\xFF\xFF\xFF\xFF\xFF\xFF", "enp3s0f2", "CheckIn")
			if mac:
				print "Got a new node: " +  mac + "\n"
		except KeyboardInterrupt:
			notifier.stop()
			print 'KeyboardInterrupt caught'
			raise
		except:
			pass

@app.route('/')
def root():
	return app.send_static_file('index.html') 
	# return "hello"

@app.route("/api")
def show_user_profile():
	message = request.args.get("m");
	message = str(message)
	if message == None:
		message = "hey there"
	count = 0
	attempts = 10
	while count < attempts:
		if Packet.sendPacket("\x78\x24\xaf\x10\x34\x44", "\x00\x1b\x24\x07\x57\x9e", message, "enp3s0f2"):
			return "Succesful Transmission"
		else:
			pass
		count+=1
	return "unsuccessful"
if __name__ == '__main__':
	thread = threading.Thread(target=startListener, args = ())
	thread.daemon = True
	thread.start()
	app.debug = True
	# app.run()
	app.run(host='0.0.0.0')