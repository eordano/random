#! /bin/env python2.5
import sys, os
from time import time
from math import pow

if __name__ == '__main__':
	os.system('g++ -o generar generar.cpp -O3')
	os.system('g++ -o floyd floyd.cpp -O3')
	salida = open('tiempos.log','w')
	j = 1.0
	tiempopy = 0.0
	while tiempopy < 20:
		j += 0.5
		nodos = pow(2, j)
		print('Orden 2^%g:'%(j))
		tiempoc = 0.0
		tiempopy = 0.0
		for i in range(4):
			n = nodos
			os.system('echo %d > ca/caso%d.gen'%(n, j*4+i))
			os.system('./generar < ca/caso%d.gen > ca/caso%d.in'%(j*4+i,j*4+i))
			print('\tCaso %d'%(j*4+i))
			tiempo = time()
			os.system('./floyd < ca/caso%d.in > ca/caso%d.cpp.out'%(j*4+i,j*4+i))
			print('\tEn C++:\t\t caso %d %f segundos'%(j*4+i, time()-tiempo))
			tiempoc += time()-tiempo
			tiempo = time()
			os.system('python floyd.py < ca/caso%d.in > ca/caso%d.py.out'%(j*4+i,j*4+i))
			print('\tEn Python:\t caso %d %f segundos'%(j*4+i, time()-tiempo))
			tiempopy += time()-tiempo
			if os.system('diff ca/caso%d.py.out ca/caso%d.cpp.out 2> /dev/null'%(j*4+i,j*4+i)):
				os.system('echo "\t\tERROR"')
		salida.write('%f %f %f\n' % (j, tiempoc/4, tiempopy/4))
