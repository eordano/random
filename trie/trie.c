#include "trie.h"
#include <errno.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>

typedef struct {
    
    void* data;
    int childs;
    int words[NUM_VALID_CHARS];
} trie_node_t;

typedef struct {

    int root;
} itrie_t;

static const int INITIAL_SPACE = 15;
static int* available_spaces = NULL;
static trie_node_t* sp = NULL;
static int first_available = -1;
static int size_allocd = 0;
static bool first_request = true;
static int trie_count = 0;

static inline bool is_valid_char(char c) {
    
    if ('a' <= c && c <= 'z') return true;
    if ('A' <= c && c <= 'Z') return true;
    if ('0' <= c && c <= '9') return true;
    if (c == '_' || c == '.' ) return true;
    return false;
}

static inline int char_to_index(char c) {

    if ('0' <= c && c <= '9') return c - '0';
    if ('a' <= c && c <= 'z') return (c - 'a') + 10;
    if ('A' <= c && c <= 'Z') return (c - 'A') + 36;
    switch(c) {
        case '_':
            return 62;
        case '.':
            return 63;
        default:
            return -1;
    }
}

static inline char index_to_char(int c) {
    if (c < 10) return '0'+c;
    if (c < 36) return 'a'+c-10;
    if (c < 62) return 'A'+c-36;
    if (c == 62) return '_';
    if (c == 63) return '.';
    return '!';
}

static int new_node() {

    if (first_request) {
        
        size_allocd = INITIAL_SPACE;
        available_spaces = (int*)malloc(sizeof(int)*size_allocd);
        if (available_spaces == NULL) {
            return -1;
        }
        sp = (trie_node_t*)malloc(sizeof(trie_node_t)*size_allocd);
        if (sp == NULL) {
            return -1;
        }
        for (int i = 0; i < size_allocd; i++) {

            available_spaces[++first_available] = i;
        }
        first_request = false;
    }
    if (first_available == 0) {

        size_allocd *= 2;
        available_spaces = realloc(available_spaces, sizeof(int)*size_allocd);
        if (available_spaces == NULL) {
            return -1;
        }
        sp = realloc(sp, sizeof(trie_node_t)*size_allocd);
        if (sp == NULL) {
            return -1;
        }
        for(int i = size_allocd / 2; i < size_allocd; i++) {
            
            available_spaces[++first_available] = i;
        }
    }
    return available_spaces[first_available--];
}

static void free_node(int node) {
    
    available_spaces[++first_available] = node;
}

trie_t new_trie() {
    
    trie_count++;
    
    /* Malloc trie... */
    itrie_t* trie = (itrie_t*)malloc(sizeof(trie_t));
    if (trie == NULL) {
        return NULL;
    }

    /* Malloc root... */
    trie->root = new_node();
    if (trie->root == -1) {
        free(trie);
        return NULL;
    }

    /* Init root */
    (sp+trie->root)->data = NULL;
    (sp+trie->root)->childs = 0;
    memset((sp+trie->root)->words, -1, sizeof(void*)*NUM_VALID_CHARS);

    return trie;
}

bool add_kv(trie_t trie, char* key, void* value) {

    int parent_index = ((itrie_t*)trie)->root;
    int node_index;
    
    trie_node_t* parent = sp+parent_index;
    trie_node_t* node;

    int i = 0;

    while (key[i] != '\0') {
        
        if (!is_valid_char(key[i])) {
            errno = EINVAL;
            return false;
        }

        int node_index = parent->words[char_to_index(key[i])];

        /* If it's a new node, update pointers and initialize values */
        if (node_index == -1) {
            node_index = new_node();
            if (node_index == -1) {
                return false;
            }
            node = sp+node_index;
            parent = sp+parent_index;

            node->data = NULL;
            memset(node->words, -1, sizeof(int) * NUM_VALID_CHARS);
        }

        node = sp+node_index;

        parent->childs++;
        parent->words[char_to_index(key[i])] = node_index;
        parent_index = node_index;
        parent = sp+parent_index;
        ++i;
    }

    node->data = value;
    return true;
}

void* seek_k(trie_t trie, char* key) {

    trie_node_t* node = sp+(((itrie_t*)trie)->root);
    int i = 0;

    while (key[i] != '\0') {

        if (!is_valid_char(key[i])) {
            return NULL;
        }
        int node_index = node->words[char_to_index(key[i++])];
        if (node_index == -1) {
            return NULL;
        } else {
            node = sp+node_index;
        }
    }

    return node->data;
}

static bool rm_node_kv(int node_index, char* key) {

    if (*key == '\0') {

        trie_node_t* node = sp+node_index;
        node->data = NULL;
        free_node(node_index);
        return true;

    }

    if (is_valid_char(*key)) {

        trie_node_t* node = sp+node_index;
        int index = char_to_index(*key);
        int child_index = node->words[index];

        if (child_index == -1) {
            return false;
        }
        if (rm_node_kv(child_index, key+1)) {

            node->childs--;
            if (!node->childs) {
                free_node(node_index);
            }
            return true;
        }
    }
}

bool rm_k(trie_t trie, char* key) {

    trie_node_t *node = sp+(((itrie_t*)trie)->root);
    int i = 0;

    while (key[i] != '\0') {
        
        if (!is_valid_char(key[i])) {
            return false;
        }
        int node_index = node->words[char_to_index(key[i++])];
        if (node_index == -1) {
            return false;
        } else {
            node = sp+node_index;
        }
    }

    node->data = NULL;
    return true;
}

static void rec_erase_node(int node_index) {
    
    if (node_index == -1) {
        return;
    }
    trie_node_t* node = sp+node_index;
    for (int i = 0; i < NUM_VALID_CHARS; i++) {
        rec_erase_node(node->words[i]);
    }
    free_node(node_index);
}

void erase_trie(trie_t trie) {
    
    rec_erase_node(((itrie_t*)trie)->root);
    free(trie);

    if (--trie_count == 0) {
        free(available_spaces);
        free(sp);
        first_request = 0;
        first_available = -1;
        size_allocd = 0;
    }
}


static void rec_debug_trie(int index, int tabs) {

    printf("Node #%d", index);
    int cas;
    tabs++;
    for(int i = 0; i < NUM_VALID_CHARS; i++) {
        if (((sp+index)->words[i]) != -1) {
            printf("\n  ");
            for (int j = 0; j < tabs; j++) {
                printf("  ");
            }
            printf("'%c' -> ", index_to_char(i));
            rec_debug_trie((sp+index)->words[i], tabs);
        }
    }
    printf("\n");
    tabs--;
}

void debug_trie(trie_t trie) {
    rec_debug_trie(((itrie_t*)trie)->root, 0);
}

