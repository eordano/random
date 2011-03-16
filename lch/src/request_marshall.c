#include "include/request_marshall.h"

#include <string.h>
#include <stdio.h>
static int RESP_BLOCK_SIZE = 4096;

/**
 * Get a line from a string. It divides the string into two, and takes
 * the first part and copies to a new malloc'd char buffer.
 * Please remember to free that string afterwards.
 */
static char* get_line(char* raw_string){
    char* index_eol = strchr(raw_string, '\n');

    size_t line_length = index_eol - raw_string;
    char* retval = malloc(line_length + 1);
    strncpy(retval, raw_string, line_length);
    retval[line_length] = '\0';

    return retval;
}

/**
 * Takes a string that has the form:
 * "SOMETHING: OTHER THING"
 * and creates a *struct pair_strings* with a copy of both
 * SOMETHING and OTHER THING, in two different strings, into
 * the 'key' and 'value' members of the returned struct
 */
static struct pair_strings* read_pair_strings(char* raw_string){
    struct pair_strings* retval = malloc(sizeof(struct pair_strings));

    char* index_eol = strchr(raw_string, '\0');
    char* index_start_value = strchr(raw_string, ':')+2;

    size_t key_length = index_start_value - raw_string - 2;
    size_t value_length = index_eol - index_start_value;

    retval->key = malloc(key_length+1);
    retval->value = malloc(value_length+1);

    strncpy(retval->key, raw_string, key_length);
    retval->key[key_length] = 0;
    strncpy(retval->value, index_start_value, value_length);
    retval->key[value_length] = 0;

    return retval;
}

/**
 * Transform a raw string into our local data representation of a http request
 */
struct http_request_t* request_marshall(char* raw_http_request){
    struct http_request_t* retval = malloc(sizeof(struct http_request_t));

    switch(*raw_http_request){
        case 'O':
            retval->request_type = OPTIONS;
            break;
        case 'G':
            retval->request_type = GET;
            break;
        case 'H':
            retval->request_type = HEAD;
            break;
        case 'P':
            if (raw_http_request[1] == 'U'){
                retval->request_type = PUT;
            } else if (raw_http_request[1] == 'O'){
                retval->request_type = POST;
            } else {
                free(retval);
                return NULL;
            }
            break;
        case 'D':
            retval->request_type = DELETE;
            break;
        case 'T':
            retval->request_type = TRACE;
            break;
        case 'C':
            retval->request_type = CONNECT;
            break;
        default:
            free(retval);
            return NULL;
            break;
    }

    while(*(++raw_http_request) != ' ');
    char* next_space = strchr(++raw_http_request, ' ');

    retval->path = malloc(next_space - raw_http_request + 1);
    strncpy(retval->path, raw_http_request, next_space - raw_http_request);
    retval->path[next_space - raw_http_request] = 0;
    retval->host = NULL;
    retval->user_agent = NULL;
    retval->referer = NULL;

    while(*(raw_http_request++) != '\n');

    char* line;
    int first_header = 1;

    while(*(line = get_line(raw_http_request))){
        struct pair_strings *pair = read_pair_strings(line);

        if (strcmp(pair->key, "Host") == 0){
            retval->host = pair->key;
        }
        if (strcmp(pair->key, "User-Agent") == 0){
            retval->user_agent = pair->key;
        }
        if (strcmp(pair->key, "Referer") == 0){
            retval->referer = pair->key;
        }
        if (first_header){
            retval->headers = dll_new();
            retval->headers->data = pair;
            
            first_header = 0;
        } else {
            dll_add_after(retval->headers, pair);
        }

        raw_http_request = strchr(raw_http_request, '\n')+1;
        free(line);
    }
    size_t data_length = strlen(++raw_http_request);

    retval->data = malloc(data_length);
    strcpy(retval->data, raw_http_request);

    return retval;
}

/**
 * Frees allocated pair of strings
 */
static void free_pair_strings(struct pair_strings* pair){
    free(pair->key);
    free(pair->value);
    free(pair);
}

/**
 * Frees a node of a linked list containing a pair of strings
 */
static void free_link_of_pair_strings(struct dlinked_list* dll){
    free_pair_strings((struct pair_strings*)dll->data);
    dll_delete_link(dll);
}

/**
 * Method to clean up the memory taken by an HTTP request
 */
void free_http_request(struct http_request_t* request){
    free(request->path);
    free(request->host);
    free(request->user_agent);
    free(request->referer);
    free(request->data);
    free_link_of_pair_strings(request->headers);
    free(request);
}

/**
 * Method to clean up the memory taken by an HTTP response
 */
void free_http_response(struct http_response_t* response){
    free(response->content_type);
    free(response->content);
    free_link_of_pair_strings(response->footers);
    free(response);
}

/**
 * Helper with string buffers
 */
static char* write_in_buffer(char* buffer, int* where, char* what,
    size_t length, int* buffer_size)
{
    while (*where + length >= *buffer_size){
        *buffer_size = *buffer_size + RESP_BLOCK_SIZE;
        buffer = realloc(buffer, *buffer_size);
    }
    strncpy(buffer + *where, what, length);
    *where += length;

    return buffer;
}

/**
 * Write all footers into one string
 */
static char* compute_footers(struct http_response_t* response){
    if (response->footers->data == NULL){
        return "";
    }

    char* retval = malloc(RESP_BLOCK_SIZE);
    int buffer_size = RESP_BLOCK_SIZE;

    int written = 0;
    #define wr_in_buff2(w, s) retval = write_in_buffer(retval, &written, w, s, &buffer_size)

    struct dlinked_list* current = response->footers;

    do{
        struct pair_strings* pair = (struct pair_strings*) current->data;

        wr_in_buff2(pair->key, strlen(pair->key));
        wr_in_buff2(": ", 2);
        wr_in_buff2(pair->value, strlen(pair->value));
        wr_in_buff2("\n", 1);

        current = current->next;
    } while (current != response->footers);
    wr_in_buff2("\0", 1);

    return retval;
}

/**
 * Take a HTTP Response and build up a string
 */
char* request_unmarshall(struct http_response_t* response){
    char* retval = malloc(RESP_BLOCK_SIZE);
    int buffer_size = RESP_BLOCK_SIZE;

    int written = 0;
    #define wr_in_buff(w, s) retval = write_in_buffer(retval, &written, w, s, &buffer_size)
    wr_in_buff("HTTP/1.1 ", 9);
    switch(response->status_code){
        case SC_OK:
            wr_in_buff("200 OK\n", 7);
            break;
        case SC_BAD_REQUEST:
            wr_in_buff("400 Bad request\n", 16);
            break;
        case SC_NOT_FOUND:
            wr_in_buff("404 Not found\n", 14);
            break;
        case SC_SERVER_ERROR:
        default:
            wr_in_buff("500 Server error\n", 17);
            break;
    }
    wr_in_buff("Content-Type: ", 14);
    wr_in_buff(response->content_type, strlen(response->content_type));
    wr_in_buff("\n", 1);
    wr_in_buff("Content-Length: ", 16);
    char cont_length[32];
    sprintf(cont_length, "%d", response->content_length);
    wr_in_buff(cont_length, strlen(cont_length));
    wr_in_buff("\n", 1);
    char* footers = compute_footers(response);
    wr_in_buff(footers, strlen(footers));
    wr_in_buff("\n", 1);
    wr_in_buff(response->content, response->content_length);
    wr_in_buff("\0", 1);
    free_http_response(response);

    return retval;
}

