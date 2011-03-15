#ifndef __request_marshall_h__
#define __request_marshall_h__

#include <stdlib.h>

#include "http_types.h"
#include "defines.h"

struct http_request_t* request_marshall(char* raw_http_request);
char* request_unmarshall(struct http_response_t* response);

void free_http_response(struct http_response_t* response);
void free_http_request(struct http_request_t* request);

#endif // __request_marshall_h__

