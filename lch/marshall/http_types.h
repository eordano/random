#ifndef __http_types_h__
#define __http_types_h__

#include "../util/dlinked_list.h"
#include "../util/defines.h"

typedef enum {
    OPTIONS, GET, HEAD, POST, PUT,  DELETE, TRACE, CONNECT
} request_type_t;
typedef int status_code_t;

#define SC_OK 200
#define SC_BAD_REQUEST 400
#define SC_NOT_FOUND 404
#define SC_SERVER_ERROR 500

struct pair_strings{
    char* key;
    char* value;
};

struct http_request_t {
    request_type_t request_type;
    char* path;

    // Privileged headers
    char* host;
    char* user_agent;
    char* referer;

    struct dlinked_list* headers;
    char* data;
};

struct http_response_t {
    status_code_t status_code;

    char* content_type;
    size_t content_length;
    struct dlinked_list footers;

    char* content;
};

#endif // __http_types_h__

