#include "include/http_types.h"
#include "include/lch.h"
#include "include/lch_helpers.h"

#include <string.h>

struct http_response_t* handler(struct http_request_t* request){
    char* content = malloc(4098);
    strcpy(content, "<html><head><title>Exito</title></head>"
    "<body><h1>It works!</h1></body></html>\0");
    return lch_response_200(content);
}

int main(int argc, char** argv){
    int port;
    if (argc < 2) port = 2000;
    else port = atoi(argv[1]);

    init_lch(port, handler);
    return 0;
}
