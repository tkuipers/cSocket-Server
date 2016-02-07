#include "Socket.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int buildPacket(long, long, long, long, long, long, long, long, long, long, long, long, char*);
int main(){
	buildPacket(0x00,
	0x1b,
	0x24,
	0x07,
	0x57,
	0x9e,
	0x78,
	0x24,
	0xaf,
	0x10,
	0x34,
	0x44,
	"heydsaasdassd");
	return 1;

}

int buildPacket(long ClientMac0, long ClientMac1, long ClientMac2, long ClientMac3, long ClientMac4, long ClientMac5, long myMac0, long myMac1, long myMac2, long myMac3, long myMac4, long myMac5, char* message){
	
	sendPacket(ClientMac0, ClientMac1, ClientMac2, ClientMac3, ClientMac4, ClientMac5, message);
	
	if(recievePacket(myMac0, myMac1, myMac2, myMac3, myMac4, myMac5) == 1){
		printf("SUCCESFUL TRANSMISSION\n");
	}
	else{
		printf("THERE WAS A PROBLEM\n");
	}
	return 1;
}

	