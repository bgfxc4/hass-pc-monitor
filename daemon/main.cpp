#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>
#include <string>

#define PORT 5573

void error(const char *msg) {
	perror(msg);
	exit(1);
}

void handleMsg(std::string msg, int sockfd) {
	int n;
	std::string token = msg.substr(0, msg.find(' '));

	std::string response = "";
	if (token == "AUTH") {
		std::string password = msg.substr(5, msg.length()-5);
		if (password == "TestPassword") {
			response = "OK";
		} else {
			response = "ERROR Wrong password";
		}
	} else {
		response = "ERROR Wrong token";
	}

	n = write(sockfd, response.c_str(), response.length());
	if (n < 0) 
		error("ERROR writing to socket");
}

int main() {
	int sockfd, newsockfd;
	socklen_t clilen;
	char buffer[1024];
	struct sockaddr_in serv_addr, cli_addr;
	int n;

	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if (sockfd < 0) 
		error("ERROR opening socket");

	bzero((char *) &serv_addr, sizeof(serv_addr));
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = INADDR_ANY;
	serv_addr.sin_port = htons(PORT);

	if (bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0) 
		error("ERROR on binding");

	while (1) {
		listen(sockfd, 5);
		clilen = sizeof(cli_addr);
		newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
		if (newsockfd < 0)
			error("ERROR on accept");
			
		bzero(buffer,256);
		n = read(newsockfd,buffer,255);
		if (n < 0) 
			error("ERROR reading from socket");

		printf("Here is the message: %s\n",buffer);
		
		handleMsg(buffer, newsockfd);

		close(newsockfd);
	}
	close(sockfd);
	return 0; 
}