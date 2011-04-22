#ifndef _TRIE_H_
#define _TRIE_H_

#include <stdbool.h>

#define NUM_VALID_CHARS 64

typedef void* trie_t;

/*
 * Initialize a trie
 */
trie_t new_trie();

/*
 * Add a (key, value) pair.
 */
bool add_kv(trie_t trie, char* key, void* value);

/*
 * Seek the value for a given key. May return NULL if there is no key.
 */
void* seek_k(trie_t trie, char* key);

/*
 * Remove a key and its pair
 */
bool rm_k(trie_t trie, char* key);

/*
 * Free resources used by the trie
 */
void erase_trie(trie_t trie);

void debug_trie(trie_t trie);

#endif

