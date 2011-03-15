#include <stdlib.h>

#include "dlinked_list.h"

struct dlinked_list* dll_new(){
    struct dlinked_list* new_head = malloc(sizeof(struct dlinked_list));
    new_head->next = new_head;
    new_head->prev = new_head;
    new_head->data = NULL;
    return new_head;
}

int dll_is_empty(struct dlinked_list* dll){
    return dll->data == NULL && dll->next == dll->prev && dll->next == dll;
}

void dll_add_after(struct dlinked_list* dll, void* data){
    struct dlinked_list* new_link = malloc(sizeof(struct dlinked_list));
    new_link->data = data;
    new_link->prev = dll;
    new_link->next = dll->next;
    dll->next = new_link;
}

void dll_add_before(struct dlinked_list* dll, void* data){
    dll_add_after(dll->prev, data);
}

void dll_join_lists(struct dlinked_list* dll1, struct dlinked_list* dll2){
    struct dlinked_list* dll1_next = dll1->next;
    struct dlinked_list* dll2_next = dll2->next;
    dll1->next = dll2_next;
    dll2_next->prev = dll1;
    dll2->next = dll1_next;
    dll1_next->prev = dll2;
}

void dll_delete_link(struct dlinked_list* dll){
    dll->next->prev = dll->prev;
    dll->prev->next = dll->next;
    free(dll);
}

void dll_iterate(struct dlinked_list* dll, void (*callback)(void*)){
    struct dlinked_list* iter = dll;
    do{
        iter = iter->next;
        callback(iter->prev->data);
    } while (iter != dll);
}

