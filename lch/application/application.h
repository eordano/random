#ifndef __application_h__
#define __application_h__

#include <stdlib.h>

#include "../marshall/request_marshall.h"
#include "../marshall/http_types.h"
#include "../util/defines.h"
#include "../util/dlinked_list.h"

struct http_response_t* application(struct http_request_t*);

#endif // __application_h__

