#include "Socket.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){
	char* input;
    gets(input);
    int count = 0;
    int max  =10;
    while(input && count < max){  //read from STDIN (aka command-line)
        // printf("%s\n", input);  //print out what user typed in
        // memset(input, 0, strlen(input));  //reset string to all 0's
        sendPacket(CLIENT_MAC0, CLIENT_MAC1, CLIENT_MAC2, CLIENT_MAC3, CLIENT_MAC4, CLIENT_MAC5, input);
        if(recievePacket() == 1){
        	printf("SUCCESFUL TRANSMISSION\n");
            break;

        }
        else{
        	printf("THERE WAS A PROBLEM\n");
        }
        count++;
    }
    return 1;
}