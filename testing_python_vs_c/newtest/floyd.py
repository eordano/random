import sys
import numpy

if __name__ == '__main__':
	entrada = sys.stdin
	n = int(entrada.readline().split()[0])
	o = sys.stdin.readlines()
	temp = [ [ int(a) for a in x.split()] for x in o]
	m = numpy.array(temp, dtype=int)
	for k in range(n):
		for i in range(n):
			if i != k:
				for j in range(n):
					if i != j and j != k:
						if m[i,k] + m[k,j] < m[i,j]:
							m[i,j] = m[i,k] + m[k,j]
	for b in m:
		for a in b:
			sys.stdout.write(str(a)+' ')
		sys.stdout.write('\n')
