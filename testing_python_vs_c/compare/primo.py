import sys, math

def esPrimo(n):
	if n == 0 or n == 1:
		return False
	raiz = int(math.sqrt(n))+2
	for divisor in range(2, raiz):
		if n % divisor == 0:
			return False
	return True
	
esPrimo(int(sys.argv[1]))