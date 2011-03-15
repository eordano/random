#ifndef __request_marshall_h__
#define __request_marshall_h__

#include "http_types.h"

struct http_request_t request_marshall(char* raw_http_request);
char* request_unmarshall(struct http_response_t response);

#endif // __request_marshall_h__

