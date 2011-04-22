#include "trie.h"
#include <stdio.h>
#include <assert.h>

int main() {

    trie_t* trie = new_trie();

    assert(trie != NULL);

    int one = 1;
    int n;
    char s[256];
    scanf("%d", &n);

    for (int i = 0; i < n; i++) {
        scanf("%s", &s);
        assert(add_kv(trie, s, &one));
    }

    erase_trie(trie);

    return 0;
}

