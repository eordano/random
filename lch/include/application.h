#ifndef __application_h__
#define __application_h__

#include <stdlib.h>

#include "request_marshall.h"
#include "http_types.h"
#include "defines.h"
#include "dlinked_list.h"

struct http_response_t* application(struct http_request_t*);

#endif // __application_h__

