#include <stdio.h>
#include "RakNet/RakPeerInterface.h"

#define MAX_CLIENTS 10
#define SERVER_PORT 60000

int main(void)
{
	printf("Creating the RakPeerInterface...\n");
	RakNet::RakPeerInterface *peer = RakNet::RakPeerInterface::GetInstance();

	printf("(C) or (S)erver?\n");
	//char str[512];
	//gets(str);
	//const bool isClient = (str[0] == 'c') || (str[0] == 'C');
	const bool isClient = false;
	if (isClient)
	{
		RakNet::SocketDescriptor sd;
		peer->Startup(1, &sd, 1);
	}
	else
	{
		RakNet::SocketDescriptor sd(SERVER_PORT, 0);
		peer->Startup(MAX_CLIENTS, &sd, 1);
	}


	// TODO - Add code body here

	RakNet::RakPeerInterface::DestroyInstance(peer);

	return 0;
}
