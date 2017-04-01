#!/usr/bin/env python
# from socket import socket, AF_PACKET, SOCK_RAW
import socket
import struct
import sys,os
import binascii
import fcntl
import time
import random
import threading
from multiprocessing import Process

class Server:
	#SELF VARIABLES
	#myAdd = My MAC Address
	#dev = The Device to run the packets through
	#self.devices = a list of all the devices that this machine is controlling
	#self.deviceStatuses = a list of statuses of each of the devices
	#self.pollTime = the amount of time between polling devices
	#self.blackList = a list of blacklisted devices that you never want prompts for

	
	@staticmethod
	def getHwAddr(ifname):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
		return info[18:24]


	def sendPacket(self, dst, msg):
		self.sendPayload(dst, msg)
		return self.listen("Received")
	
	def sendPayload(self, dst, msg):
		s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
		s.settimeout(1.2)
		s.bind((self.dev, 0))
		
		# We're putting together an ethernet frame here, 
		# but you could have anything you want instead
		# Have a look at the 'struct' module for more 
		# flexible packing/unpacking of binary data
		# and 'binascii' for 32 bit CRC
		src_addr = self.myAdd
		dst_addr = dst
		payload = msg
		
		ethertype = "\x08\x00"
		
		s.send(dst_addr+src_addr+ethertype+payload)
	
	def listenForDevices(self):
		while True:
			try:
				# print("Listening")
				listenVar = self.listen("CheckIn", 50)
				#print "Got something"
				if listenVar:
					#code for adding device to list
					newAdd = binascii.unhexlify(listenVar[0:12])
					print "Found Device: " + listenVar[0:12]
					#check if value is already in list... if it is, automatically re-add, else ask
					if not newAdd in self.devices:
						print "Adding Device: " + listenVar[0:12]
						print "\tID: " + listenVar[13]
						time.sleep(0.3)
						# if raw_input("New Device found.  Would you like to add: " + str(listenVar[0:12]) + "?\nY or N\n") == 'Y':
						self.deviceIDs.append(listenVar[13]);
						self.devices.append(binascii.unhexlify(listenVar[0:12]))
						self.deviceStatuses.append(self.goodNumber);
						self.sendPayload(newAdd, "Accepted")
						print "Device list = " + str(self.devices)
						# return
					else:
						print "Re-registering"
						time.sleep(0.3)
						# time.sleep(1)
						# self.devices.append(binascii.unhexlify(listenVar[0:12]))
						self.sendPayload(newAdd, "Accepted")
						self.deviceStatuses.append(self.goodNumber);
					# pass
			except KeyboardInterrupt:
				notifier.stop()
				print 'KeyboardInterrupt caught'
				raise
			except Exception as inst:
				print inst
				pass

	def getDevList(self):
		outList = [];
		for i in range(0, len(self.devices)):
			outList.append([binascii.hexlify(self.devices[i]), self.deviceIDs[i]])
			# outList.append(binascii.hexlify(self.devices[i]))


		return outList	

	def pollDevices(self):
		while True:
			try:
				for i in range(0, len(self.devices)):
					deviceUp = 0;
					for j in range(1, 10):
						print "Sending Polling Signal too" + self.devices[i]
						self.sendPayload(self.devices[i], "CheckUp")
						#TODO: Needs to be changed so that after this, it removes the device from the device list
						if self.listen("Here", 2):
							print "Recieved Confirmation"
							# self.deviceStatuses[i] = 3;
							deviceUp = self.goodNumber;
							break
						else:
							break	
					time.sleep(3)
					self.deviceStatuses[i] = deviceUp
				time.sleep(self.pollTime)
				
			except KeyboardInterrupt:
				notifier.stop()
				print 'KeyboardInterrupt caught'
				raise
			except Exception as inst:
				print inst
				pass


	def listen(self,msg, time=10):
		#print "Listening\n"
		rawSocket=socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.htons(0x0003))
		rawSocket.bind((self.dev, 0))
		rawSocket.settimeout(time)
		#ifconfig eth0 promisc up
		receivedPacket=rawSocket.recv(2048)
		
		#Ethernet Header...
		ethernetHeader=receivedPacket[0:14]
		# arp_header = receivedPacket[0][14:]
		ethrheader=struct.unpack("!6s6s2s",ethernetHeader)
		destinationIP= binascii.hexlify(ethrheader[0])
		sourceIP=ethrheader[1]
		protocol= binascii.hexlify(ethrheader[2])
		# print "dest: " + destinationIP + " myAdd: " + self.myAdd + "\n"
		# print "\t" + str(binascii.hexlify(receivedPacket[0:14]))
		# print "\t" + str(receivedPacket[14:])
		# print "source: " + sourceIP + " client: " + binascii.hexlify(clientAdd)
		if destinationIP == binascii.hexlify(self.myAdd) or destinationIP == "ffffffffffff":
			# print "Destination: " + destinationIP
			# print "Source: " + sourceIP
			# print "Protocol: "+ protocol
			# print "Out: " + receivedPacket[14:] + "\n\n\n"
			if receivedPacket[14:(len(msg) + 14)]==msg:
				return receivedPacket[(len(msg) + 14):]
			else:
				#print receivedPacket[14:(len(msg) + 14)]+ " != " + msg + "\n"
				return 0
		else:
			#print "address mismatch"
			#print receivedPacket[14:22]
			return 0

	def testPacket(self):
		while True:
			try:
				print "Sending Signal too: " + self.devices[0]
				if self.sendPacket(self.devices[0], "{\"type\": lightRequest, {\"bar\":[\"baz\", null, 1.0, 2]}}"):
					print "SUCCESFUL TRANSMISSION"
				time.sleep(random.randrange(7, 15))
			except KeyboardInterrupt:
				notifier.stop()
				print 'KeyboardInterrupt caught'
				raise
			except Exception as inst:
				print inst
				pass

	def __init__(self, inDev, inTime):
		self.dev = inDev
		self.myAdd = self.getHwAddr(inDev)
		self.devices = []
		self.deviceIDs = []
		self.deviceStatuses = []
		self.goodNumber = 3
		# self.listenForDevices()
		self.pollTime = inTime
		listenThread = threading.Thread(target=self.listenForDevices)
		listenThread.start()
		pollThread = threading.Thread(target=self.pollDevices)
		pollThread.start()
		# testThread = Process(target=self.testPacket)
		while True:
			time.sleep(10)
			print "Sending test thingy"
			self.sendPacket("\x00\x00\x00\x00\x00\x00", "{\"testThingy\": 3")
		# testThread.start()
		print str(self.devices)
		pass


if __name__ == '__main__':
	print "Cannot interact with this module directly"
