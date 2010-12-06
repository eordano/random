#include <set>
#include <iostream>
#include <map>
#include <string>
#include <cstdlib>
#include <cstdio>
#include <ctime>
using namespace std;

int main(){
	int N, M;
	scanf("%d %d", &N, &M);
    srand(time(NULL));
	printf("%d %d\n", N, M);
    for(int i = 0; i < M; i++){
		printf("%d %d\n", rand()%N, rand()%N);
    }
    return 0;
}
