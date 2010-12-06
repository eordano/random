# -*- coding: utf-8 -*-
import os

from generation import Generation
from puntos import Puntos

G = Generation(Puntos)

def make_plot(fittest):
	ret = ""
	for point in fittest.conjunto:
		ret += str(point[0])+ " " + str(point[1]) + "\n"
	return ret

def average(ls):
	return sum(ls)/len(ls)

cont = 0

while True:
	G = G.spawn_new_gen()
	cont += 1
	if (cont % 40 == 1):
		fittest = max([(ind.fitness(), ind) for ind in G.individuals])[1]
		fitness = fittest.fitness()
		data_output = open('data.out', 'w')
		graph_guide = open('graph.gnp', 'w')
		data_output.write(make_plot(fittest))
		graph_guide.writelines([ "set terminal png size 800,600\n",
			"set output './images/fittest%d.png'\n"%(cont/40),
			"set xrange [0:20]\n", "set yrange [0:20]\n",
			"set label 1 'Fitness = %f' at 1,1\n"%fitness,
			"plot './data.out' using 1:2 title 'Generation %d' with points pt 7 lt 2 lw 2 \n"%(cont/40)])
		data_output.close()
		graph_guide.close()
		os.system('gnuplot graph.gnp')
