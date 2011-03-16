#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "include/request_marshall.h"
#include "../include/lch.h"
#include "../include/http_types.h"

const int BLOCK_SIZE = 4096;

/**
 * Main function that will initialize the socket listening and sits
 * waiting for connections, when it gets one, spawns a thread and asks
 * him to handle the connection
 *
 */
void init_lch(int port, struct http_response_t* (*callback)(struct http_request_t* req)){

    // Create the binding to the port specified as first argument
    int socket_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (socket_fd < 0){
        printf("Error creating socket\n");
        exit(1);
    }

    // Setup the socket address
    struct sockaddr_in socket_address;
    memset(&socket_address, 0, sizeof(socket_address));
    socket_address.sin_family = AF_INET;
    socket_address.sin_addr.s_addr = INADDR_ANY;
    socket_address.sin_port = htons(port);

    // Bind to the port
    if (bind(socket_fd, (struct sockaddr *) &socket_address,
        sizeof(socket_address)) < 0)
    {
        printf("Error binding to port\n");
        exit(1);
    }

    // We are listening
    listen(socket_fd, 5);
    
    // Get those connections!
    for( ; ; ){

        // This locks my process, so the infinite loop is not that heavy
        int new_socket_fd = accept(socket_fd, NULL, NULL);

        int pid = fork();
        if (pid > 0){ 
            continue;
        } else if (pid < 0){
            printf("Error forking process. Aborting.\n");
            exit(1);
        }

        char* buffer = malloc(BLOCK_SIZE);
        int current_buffer_size = BLOCK_SIZE;
        int read_size = 0;


        read_size = recv(new_socket_fd, buffer, current_buffer_size, 0);
        if (read_size == current_buffer_size){
            do {
                current_buffer_size += BLOCK_SIZE;
                buffer = realloc(buffer, current_buffer_size);
                read_size = recv(new_socket_fd, (void*) (buffer + current_buffer_size - BLOCK_SIZE), BLOCK_SIZE, 0);
            } while (read_size == BLOCK_SIZE);
        }

        struct http_request_t* http_request = request_marshall(buffer);
        free(buffer);

        struct http_response_t* http_response = callback(http_request);
        free_http_request(http_request);

        char* response = request_unmarshall(http_response);
        free_http_response(http_response);

        write(new_socket_fd, response, strlen(response));
        free(response);

        exit(0);
    }
}

