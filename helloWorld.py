from flask import Flask
from flask import request
from flask import render_template
from flask_socketio import SocketIO
import urllib2

import json
import socket
import struct
import sys,os
import binascii
import fcntl
import time
import random
import threading
from Server import Server
from multiprocessing import Process

import lxml
from lxml.html.clean import Cleaner

app = Flask(__name__)
socketio = SocketIO(app)
app._static_folder = "/home/tyler/Documents/SmartHome/cSocket-Server/"

@app.route('/')
def root():
	return app.send_static_file('index.html') 
	# return "hello"

@socketio.on('checkForNew')
def handle_message(message):
	print "got check request"
	print str(json.dumps(server.getDevList()));
	socketio.emit("deviceList", str(json.dumps(server.getDevList())))# {"list": server.getDevList()})
	# print json.dumps(server.getDevList());
	pass
	
	# print('received message: ' + str(message))


@app.route("/message")
def sendMessage():
	message = request.args.get("m");
	address = request.args.get("d");
	print "Sending user packet to " + str(address)

	if server.sendPacket(binascii.unhexlify(str(address)), str(message)):
		print "Success"
	return "Success"

@app.route("/devicelist")
def showDevList():
	out = str(json.dumps(server.getDevList()));
	print out
	return out

@app.route("/devlookup")
def lookUpDev():
	try:
		deviceID = request.args.get("id");
		r = urllib2.urlopen("http://perfectplan.me:5000/dev?id=" + deviceID).read()
		return r
	except Exception as inst:
		print inst
		raise



if __name__ == '__main__':
	# app.debug = True
	server = Server("enp3s0f2", 5);
	# server = Server("wlp2s0f0", 5);
	# testThread.start()
	socketio.run(app, host='0.0.0.0')