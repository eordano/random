#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>

#define MAXPASOS 10000
#define ITERATIONS 10000
#define DIM 1

int pasos[DIM][MAXPASOS];
int anterior[DIM];
bool llego;
int n;

inline int realrand(){
	if (DIM == 3) {
		int a = RAND_MAX;
		while (a >= RAND_MAX - 1) a = rand();
		return a;
	} else {
		return rand();
	}
}

void pasosBorracho(void) {
	llego = false;

	for(int i = 0; i < DIM; i++) {
		pasos[i][0] = 0;
	}

	for(n = 0; !llego && n < MAXPASOS; n++) {
		for(int i = 0; i < DIM; i++) {
			anterior[i] = pasos[i][n];
		}
		int direccion = realrand()%DIM;
		int delta = 1;
		if (realrand() % 2)
			delta = -1;

		anterior[direccion] += delta;

		for(int i = 0; i < DIM; i++) 
			pasos[i][n+1] = anterior[i];
		
		bool yallego = true;
		for (int i = 0; yallego && i < DIM; i++)
			if (anterior[i] != 0)
				yallego = false;
		
		if (yallego)
			llego = true;
	}
}

int main() {

	srand(time(NULL));

	for(int i = 0; i < ITERATIONS; i++) {
		pasosBorracho();
		if (n != MAXPASOS) {
			for(int i = 0; i <= n; i++)  {
				for (int j = 0; j < DIM; j++) {
					printf("%d ", pasos[j][i]);
				}
				printf("\n");
			}
		} else {
			printf("0\n");
		}
		printf("\n");
	}
}

