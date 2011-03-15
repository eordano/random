#ifndef __dlinked_list_h__
#define __dlinked_list_h__

#include "../util/defines.h"

struct dlinked_list{
    void* data;
    struct dlinked_list *next;
    struct dlinked_list *prev;
};

struct dlinked_list* dll_new();
int dll_is_empty(struct dlinked_list* dll);
void dll_add_after(struct dlinked_list* dll, void* data);
void dll_add_before(struct dlinked_list* dll, void* data);
void dll_join_lists(struct dlinked_list* dll1, struct dlinked_list* dll2);
void dll_delete_link(struct dlinked_list* dll);
void dll_iterate(struct dlinked_list* dll, void (*callback)(void*));

#endif //__dlinked_list_h__

