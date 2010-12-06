#include <cstdlib>
#include <cstdio>
#include <ctime>
using namespace std;

int main(){
	int N;
	scanf("%d", &N);
    srand(time(NULL));
	printf("%d\n", N);
    for(int i = 0; i < N; i++){
		for(int j = 0; j < N; j++)
			printf("%d ", rand()%345123);
		printf("\n");
    }
    return 0;
}
