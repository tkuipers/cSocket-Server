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




if __name__ == '__main__':
	# app.debug = True
	server = Server("enp1s0", 5);
	# server = Server("wlp2s0f0", 5);
	# testThread.start()
