import sys
import numpy

if __name__ == '__main__':
	entrada = sys.stdin
	n = int(entrada.readline().split()[0])
	tem = [ a for a in [[ int(x) for x in sys.stdin.readline().split()] for b in range(n)] ]
	m = numpy.array(tem, dtype=int)
	for k in range(n):
		for i in range(n):
			if i != k:
				for j in range(n):
					if i != j and j != k:
						if m[i,k] + m[k,j] < m[i,j]:
							m[i,j] = m[i,k] + m[k,j]
	for a in range(n):
		for b in range(n):
			sys.stdout.write(str(m[a,b])+' ')
		sys.stdout.write('\n')
