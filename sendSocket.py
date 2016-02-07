#!/usr/bin/env python
from socket import socket, AF_PACKET, SOCK_RAW

def sendSocket(src, dst, msg):
	s = socket(AF_PACKET, SOCK_RAW)
	s.bind(("enp3s0f2", 0))
	
	# We're putting together an ethernet frame here, 
	# but you could have anything you want instead
	# Have a look at the 'struct' module for more 
	# flexible packing/unpacking of binary data
	# and 'binascii' for 32 bit CRC
	src_addr = src#"\x78\x24\xaf\x10\x34\x44"
	dst_addr = dst#"\x00\x1b\x24\x07\x57\x9e"
	payload = msg#("["*30)+"PAYLOAD"+("]"*30)
	
	ethertype = "\x08\x00"
	
	s.send(dst_addr+src_addr+ethertype+payload)

if __name__ == '__main__':
	# app.debug = True
	# app.run()
	sendSocket("\x78\x24\xaf\x10\x34\x44", "\x00\x1b\x24\x07\x57\x9e", "hey tehre");