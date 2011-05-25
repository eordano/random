if __name__ == '__main__':

	input = raw_input("Input file: ")
	output = raw_input("Output file: ")

	e = open(input, 'r').readlines()
	sizes = []
	n = 0

	for i in e:
		if i == '\n':
			if n != 0:
				sizes.append(n)
			n = 0
		else:
			n += 1
	
	f = open(output, 'w')
	
	for i in sizes:
		f.write('%d\n'%i)

	f.close()

