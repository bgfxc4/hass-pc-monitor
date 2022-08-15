#include <stdio.h>
#include <iostream>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>
#include <string>
#include "json.hpp"

#define PORT 5573

void error(const char *msg) {
	perror(msg);
	exit(1);
}

void handleMsg(std::string msg, int sockfd) {
	int n;
	std::cout << msg << std::endl;
	nlohmann::json jsonMsg = nlohmann::json::parse(msg);
	std::string token = jsonMsg["token"];

	nlohmann::json response;
	if (token == "auth") {
		std::string password = jsonMsg["password"];
		if (password == "TestPassword") {
			response["msg"] = "OK";
			response["status"] = 200;
		} else {
			response["msg"] = "ERROR Wrong password";
			response["status"] = 401;
		}
	} else {
		response["msg"] = "ERROR Wrong token";
		response["status"] = 400;
	}

	std::string responseStr = response.dump();
	n = write(sockfd, responseStr.c_str(), responseStr.length());
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