#ifndef __request_marshall_h__
#define __request_marshall_h__

#include "http_types.h"

void init_lch(int port, struct http_response_t* (*callback)(struct http_request_t* req));

#endif // __request_marshall_h__

