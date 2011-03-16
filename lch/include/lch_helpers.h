#ifndef __lch_helpers__
#define __lch_helpers__

#include "http_types.h"

struct http_response_t* lch_response_200(char* content);
// struct http_response_t* lch_response_301(char* url);
// struct http_response_t* lch_response_307(char* url);
// struct http_response_t* lch_response_404(char* content);
// struct http_response_t* lch_response_500(char* content);

#endif // __lch_helpers__

