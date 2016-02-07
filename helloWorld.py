from flask import Flask
from flask import request
import intSender as Packet
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello World!'

@app.route('/user', methods=['GET', 'POST'])
def show_user_profile():
	message = request.args.get("m");
	Packet.sendPacket(0x00, 0x1b, 0x24, 0x07, 0x57, 0x9e, 0x78, 0x24, 0xaf, 0x10, 0x34, 0x44, message);
	return 'User ' + str(username) + " pass: " + str(password)

if __name__ == '__main__':
	app.debug = True
	app.run()