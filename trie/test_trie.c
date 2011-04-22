#include "trie.h"
#include <stdio.h>
#include <assert.h>

int main() {


    int vec[] = { 0, 2, 4, 8, 16 };
    
    trie_t* trie = new_trie();

    assert(trie != NULL);

    assert(add_kv(trie, "hola", (void*)(vec)));
    assert(add_kv(trie, "chau", (void*)(vec+1)));
    assert(add_kv(trie, "hola1", (void*)(vec+2)));
    assert(add_kv(trie, "chau_", (void*)(vec+3)));

    debug_trie(trie);
    
    assert(seek_k(trie, "hola") == (void*)vec);
    assert(seek_k(trie, "chau") == (void*)(vec+1));
    assert(seek_k(trie, "hola1") == (void*)(vec+2));
    assert(seek_k(trie, "chau_") == (void*)(vec+3));
    
    assert(rm_k(trie, "chau_"));
    assert(seek_k(trie, "chau") == (void*)(vec+1));
    assert(rm_k(trie, "chau"));
    assert(!seek_k(trie, "chau"));

    erase_trie(trie);

    return 0;
}

