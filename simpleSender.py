import sendSocket as Packet
def main():
	Packet.sendPacket( "\x78\x24\xaf\x10\x34\x44", "\x00\x1b\x24\x07\x57\x9e", "hey you guy7", "enp3s0f2");
		# Packet.sendPacket("\x00\x1b\x24\x07\x57\x9e", "\x78\x24\xaf\x10\x34\x44", "hey you guy7", "wlp2s0f0");

if __name__ == "__main__":
	main()