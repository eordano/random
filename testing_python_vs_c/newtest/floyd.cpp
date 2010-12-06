#include <cstdio>
#include <vector>
using namespace std;

int main(){
	int n;
	scanf("%d", &n);
	vector<vector<int> > V(n, vector<int>(n));
	for(int i = 0; i < n; i++)
		for(int j = 0; j < n; j++)
			scanf("%d", &V[i][j]);
	for(int k = 0; k < n; k++)
		for(int i = 0; i < n; i++)
			if (i != k)
				for(int j = 0; j < n; j++)
					if (i != j && j != k)
						if (V[i][k] + V[k][j] < V[i][j])
							V[i][j] = V[i][k] + V[k][j];
	for(int i = 0; i < n; i++){
		for(int j = 0; j < n; j++)
			printf("%d ", V[i][j]);
		printf("\n");
	}
	return 0;
}
