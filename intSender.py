import ctypes
import sys

buildPacket = ctypes.CDLL('./libIntSender.so')
buildPacket.buildPacket.argtypes = (ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_char_p);


def sendPacket(client0, client1, client2, client3, client4, client5, myMac0, myMac1, myMac2, myMac3, myMac4, myMac5, message):
	global buildPacket
	# array_type = ctypes.c_int * num_numbers
	result = buildPacket.buildPacket(ctypes.c_long(long(client0)),
						ctypes.c_long(long(client1)),
						ctypes.c_long(long(client2)),
						ctypes.c_long(long(client3)),
						ctypes.c_long(long(client4)),
						ctypes.c_long(long(client5)),
						ctypes.c_long(long(myMac0)),
						ctypes.c_long(long(myMac1)),
						ctypes.c_long(long(myMac2)),
						ctypes.c_long(long(myMac3)),
						ctypes.c_long(long(myMac4)),
						ctypes.c_long(long(myMac5)),
						message);
	return int(result)


