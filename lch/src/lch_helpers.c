#include "../include/lch_helpers.h"

#include <sys/types.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>

static char* get_date();
static struct http_response_t* lch_generic_response(status_code_t status_code, char* content);

struct http_response_t* lch_response_200(char* content){
    return lch_generic_response(SC_OK, content);
}

static struct http_response_t* lch_generic_response(status_code_t status_code, char* content){
    struct http_response_t* retval = malloc(sizeof(struct http_response_t));

    retval->status_code = SC_OK;
    retval->content_type = malloc(10);
    strcpy(retval->content_type, "text/html");
    retval->footers = dll_new();

    retval->content_length = strlen(content);
    retval->content = malloc(retval->content_length + 1);
    strcpy(retval->content, content);
    retval->content[retval->content_length] = '\0';

    retval->footers = dll_new();

    retval->footers->data = malloc(sizeof(struct pair_strings));
    ((struct pair_strings*)(retval->footers->data))->key =
        malloc(sizeof("Date") + 1);
    strcpy(((struct pair_strings*)(retval->footers->data))->key, "Date");
    ((struct pair_strings*)(retval->footers->data))->value = get_date();

    return retval;
}

/** 
 * Call to posix function date
 */
char* get_date(){
    char* date = malloc(512);

    int child_pipe[2];

    pipe(child_pipe);

    int pid = fork();
    if (!pid){
        // Close stdin, stdout, stderr, for we won't use them
        close(0);
        close(1);
        close(2);
        close(child_pipe[0]);

        // And use our internal pipes
        dup2(child_pipe[1], 1); // The new stdout is pipe_out

        execl("/bin/date", "date", "-R", NULL);
    }

    close(child_pipe[1]);
    read(child_pipe[0], date, 512);
    close(child_pipe[0]);

    return date;
}

