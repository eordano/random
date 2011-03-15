#include "application.h"

#include <string.h>

struct http_response_t* application(struct http_request_t* request){
    struct http_response_t* retval = malloc(sizeof(struct http_response_t));

    retval->status_code = SC_OK;
    retval->content_type = malloc(10);
    strcpy(retval->content_type, "text/plain");
    retval->footers = dll_new();

    retval->content_length = strlen(request->data);
    retval->content = malloc(retval->content_length + 1);
    strcpy(retval->content, request->data);
    retval->content[retval->content_length] = '\0';

    free_http_request(request);

    return retval;
}

