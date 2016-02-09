#!/usr/bin/env python
# from socket import socket, AF_PACKET, SOCK_RAW
import socket
import struct
import sys,os
import binascii

class Server:
	def sendPacket(src, dst, msg, dev):
		# dev="enp3s0f2"
		# socket.setdefaulttimeout(01.2)
		sendSocket(src, dst, msg, dev)
		return listen(src, dst, dev, "Received")
	
	def sendSocket(src, dst, msg, dev):
		s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
		s.settimeout(01.2)
		s.bind((dev, 0))
		
		# We're putting together an ethernet frame here, 
		# but you could have anything you want instead
		# Have a look at the 'struct' module for more 
		# flexible packing/unpacking of binary data
		# and 'binascii' for 32 bit CRC
		src_addr = src
		dst_addr = dst
		payload = msg
		
		ethertype = "\x08\x00"
		
		s.send(dst_addr+src_addr+ethertype+payload)
	
	
	
	
	def listen(clientAdd, myAdd, dev, msg):
		rawSocket=socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.htons(0x0800))
		rawSocket.bind((dev, 0))
		rawSocket.settimeout(01.2)
		#ifconfig eth0 promisc up
		receivedPacket=rawSocket.recv(2048)
		
		#Ethernet Header...
		ethernetHeader=receivedPacket[0:14]
		# arp_header = receivedPacket[0][14:]
		ethrheader=struct.unpack("!6s6s2s",ethernetHeader)
		destinationIP= binascii.hexlify(ethrheader[0])
		sourceIP= binascii.hexlify(ethrheader[1])
		protocol= binascii.hexlify(ethrheader[2])
		# print "dest: " + destinationIP + " myAdd: " + binascii.hexlify(myAdd)
		# print "source: " + sourceIP + " client: " + binascii.hexlify(clientAdd)
		if destinationIP == binascii.hexlify(myAdd) and sourceIP == binascii.hexlify(clientAdd):
			print "Destination: " + destinationIP
			print "Source: " + sourceIP
			print "Protocol: "+ protocol
			print "Out: " + receivedPacket[14:] + "\n\n\n"
			if receivedPacket[14:(len(msg) + 14)]==msg:
				return receivedPacket[(len(msg) + 14):]
			else:
				print receivedPacket[14:(len(msg) + 14)]+ " != " + msg + "\n"
				return 0
		else:
			print "address mismatch"
			print receivedPacket[14:22]


if __name__ == '__main__':
	# :
	try:
		if sendPacket("\x78\x24\xaf\x10\x34\x44", "\x00\x1b\x24\x07\x57\x9e", "hey tehre", "enp3s0f2"):
			print "SUCCESFUL"
		else:
			print "PROBLEM"
	except Exception as inst:
		print inst
		pass