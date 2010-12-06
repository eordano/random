#include <vector>
#include <string>
#include <list>
#include <map>
#include <cstring>
#include <cstdio>
#include <list>
using namespace std;
static int distancia[10000], done[10000], queue[10000];
static int A, B;
static int N, M, n;

int main(){
    scanf("%d %d", &N, &M);
    vector<list<int> > edges(N);
    for(int i = 0; i < M; i++){
        scanf("%d %d", &A, &B);
        edges[A].push_front(B);
    }
    memset(distancia, -1, sizeof distancia);
    int b = 0, e = 0;
    queue[e++] = 0;
    distancia[0] = 0;
    done[0] = true;
    while(b < e){
        n = queue[b++];
        for(list<int>::iterator it = edges[n].begin(); it != edges[n].end(); ++it){
            if (!done[*it]){
                distancia[*it] = distancia[n]+1;
                queue[e++] = *it;
                done[*it] = true;
            }
        }
    }
    for(int i = 0; i < N; i++)
        printf("distancia a %d es %d\n", i, distancia[i]);
    return 0;
}

