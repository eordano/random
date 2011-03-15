#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "request_handler.h"

const int BLOCK_SIZE = 4096;

/**
 * Main function that will initialize the socket listening and sits
 * waiting for connections, when it gets one, spawns a thread and asks
 * him to handle the connection
 *
 */
int main(int argc, char** argv){

    // Initialize a buffer to be used to fetch data
    char* buffer = malloc(BLOCK_SIZE);
    int current_buffer_size = BLOCK_SIZE;
    int read_size = 0;

    // Validate that I got a port number
    if (argc < 2){
        printf("Usage: %s [port]\n", argv[0]);
    }

    // Create the binding to the port specified as first argument
    int port = atoi(argv[1]);
    int socket_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (socket_fd < 0){
        printf("Error creating socket\n");
    }

    // Setup the socket address
    struct sockaddr_in socket_address;
    memset(&socket_address, 0, sizeof(socket_address));
    socket_address.sin_family = AF_INET;
    socket_address.sin_addr.s_addr = INADDR_ANY;
    socket_address.sin_port = htons(port);

    // Setup address for the client that connects to us
    struct socklen_t client_length;
    struct sockaddr_in client_address;

    // Bind to the port
    if (bind(socket_fd, (struct sockaddr *) &socket_address,
        sizeof(socket_address)) < 0)
    {
        printf("Error binding to port\n");
    }

    // We are listening
    listen(socket_fd, 5);
    
    // Get those connections!
    for( ; ; ){

        // This locks my process, so the infinite loop is not that heavy
        client_length = sizeof(client_address);
        int new_socket_fd = accept(socket_fd,
            (struct sockaddr *) &client_address,
            &client_length
        );

        int pid = fork();
        if (pid > 0){ 
            continue;
        } else if (pid < 0){
            printf("Error forking process. Aborting.\n");
            return 1;
        }

        read_size = recv(new_socket_fd, buffer, current_buffer_size, 0);
        if (read_size == current_buffer_size){
            do {
                current_buffer_size += BLOCK_SIZE;
                buffer = realloc(buffer, current_buffer_size);
                read_size = recv(new_socket_fd, (void*) (buffer + current_buffer_size - BLOCK_SIZE), BLOCK_SIZE, 0);
            } while (read_size == BLOCK_SIZE);
        }

        char* response = request_handler(buffer);
        write(new_socket_fd, (void*) response, strlen(response));
        return 0;
    }

    return 0;
}

