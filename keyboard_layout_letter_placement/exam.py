#! /usr/bin/env /usr/bin/python
import sys, os

if __name__ == '__main__':
	arch = open(sys.argv[1])

	mapa = {}
	for line in arch:
		for letra in line:
			if letra.isalpha():
				if mapa.has_key(letra.upper()):
					mapa[letra.upper()] += 1
				else:
					mapa[letra.upper()] = 1

	salida = sys.stdout
	for letra in mapa:
		salida.write(letra+' '+str(mapa[letra])+'\n')
