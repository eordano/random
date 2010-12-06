#include <iostream>
#include <cmath>
#include <string>
#include <sstream>

using namespace std;

bool esPrimo(int n){
	if (n == 0 || n == 1)
		return false;
	int raiz = (int)sqrt(n)+2;
	for(int divisor = 2; divisor < raiz; divisor++)
		if (n % divisor == 0)
			return false;
	return true;
}

int main(int argc, char* argv[]){
	int n = 0;
	for(int i = 0; argv[1][i] != '\0' ; i++){
		n *= 10;
		n += argv[1][i]-'0';
	}
	n/=10;
	return esPrimo(n);
}
