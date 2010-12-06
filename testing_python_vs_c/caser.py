# -*- coding: utf-8 -*-
import sys, os
from time import time

if __name__ == '__main__':
	os.system('g++ -o tester tester.cpp -O3')
	os.system('g++ -o grafo grafo.cpp -O3')
	salida = open('tiempos.log','w')
	j = 3
	while j <= 13:
		j += 1
		nodos = 1 << j 
		print('Orden 2^%d:' % j)
		tiempoc = 0.0
		tiempopy = 0.0
		for i in range(4):
			n, m = [nodos, int(nodos**1.5)]
			os.system('echo %d %d > casos/caso%d.gen'%(n, m, j*4+i))
			tiempo = time()
			os.system('./tester < casos/caso%d.gen > casos/caso%d.in'%(j*4+i,j*4+i))
			print('\tGenerar el caso random tomó %f segundos'%(time()-tiempo))
			tiempo = time()
			os.system('./grafo < casos/caso%d.in > casos/caso%d.cpp.out'%(j*4+i,j*4+i))
			print('\tEn C++:\t\t caso %d %f segundos'%(j*4+i, time()-tiempo))
			tiempoc += time()-tiempo
			tiempo = time()
			os.system('python -OO grafo.py < casos/caso%d.in > casos/caso%d.py.out'%(j*4+i,j*4+i))
			print('\tEn Python:\t caso %d %f segundos'%(j*4+i, time()-tiempo))
			tiempopy += time()-tiempo
			if os.system('diff casos/caso%d.py.out casos/caso%d.cpp.out 2> /dev/null'%(j*4+i,j*4+i)):
				os.system('echo "\t\tERROR"')
		salida.write('%d %f %f\n' % (j, tiempoc/4, tiempopy/4))
