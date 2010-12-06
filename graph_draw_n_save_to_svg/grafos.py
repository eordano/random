# -*- coding: iso-8859-1 -*-

import pygame, math, sys

Nada, Nodo_Sel, Edge_Sel, Crea_Nodo, Crea_Edge, Eliminando = range(0,6)
Infty = 987654321

def distancia(a, b):
	if a == None or b == None:
		return Infty
	return math.sqrt((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1]))

def dist_line(punto, linea):
	return Infty

def grabar(nodos, edges, labels):
	archivo = open("test.svg", 'w')
	archivo.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
	archivo.write("<svg width=\"640\" height=\"460\">\n")
	archivo.write("\t<g>\n")
	
	for edge in edges:
		archivo.write("\t\t<line x1=\""+str(edge[0][0])+"\" y1=\"")
		archivo.write(str(edge[0][1])+"\" x2=\""+str(edge[1][0])+"\" y2=\"")
		archivo.write(str(edge[1][1])+"\" style=\"stroke:rgb(0,0,0);stroke-width=2\" />\n")
	for nodo in nodos:
		archivo.write("\t\t<circle cx=\""+str(nodo[0])+"\" cy=\"")
		archivo.write(str(nodo[1])+"\" r=\"10\" stroke=\"black\" ")
		archivo.write("stroke-width=\"2\" fill=\"white\"/>\n")
	archivo.write("\n")
	for label in labels:
		pass
	
	archivo.write("\t</g>\n")
	archivo.write("</svg>\n")

if __name__ == '__main__':
	pygame.init()
	pygame.font.init()
	nodos = []
	edges = []
	labels = []
	selnodo = None
	seledge = None
	marknodo = None
	markedge = None
	estado = Nada
	
	screen = pygame.display.set_mode((640,460))
	arial = pygame.font.match_font('arial')
	mensaje = "Todo inicializado correctamente"

	while True:
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				sys.exit()
			if evento.type == pygame.MOUSEMOTION:
				for nodo in nodos:
					if distancia(evento.pos, nodo) < distancia(evento.pos, selnodo):
						selnodo = nodo
				if distancia(evento.pos, selnodo) > 30: #Distancia arbitraria
					selnodo = None
				if selnodo == None:
					for edge in edges:
						if dist_line(evento.pos, edge) < distancia(evento.pos, seledge):
							seledge = edge
					if dist_line(evento.pos, seledge) > 20:
						seledge = None

			if evento.type == pygame.MOUSEBUTTONDOWN:
				if estado == Crea_Nodo:
					if selnodo != None:
						mensaje = "Alejarse del nodo actual!"
					else:
						nodos.append((evento.pos[0], evento.pos[1]))
						estado = Nada
				elif estado == Crea_Edge:
					if marknodo != None and selnodo != None and marknodo != selnodo:
						#crearedge(edges, marknodo, selnodo)
						edges.append((marknodo, selnodo))
					marknodo = None
					markedge = None
					estado = Nada
				elif estado == Eliminando:
					if selnodo != None:
						for nodo in nodos:
							if nodo == selnodo:
								nodos.remove(nodo)
								for edge in edges:
									if edge[0] == nodo or edge[1] == nodo:
										edges.remove(edge)
								selnodo = None
					if seledge != None:
						for edge in edges:
							if edge == seledge:
								edges.remove(edge)
								seledge = None
					estado = Nada
				else:
					if selnodo != None:
						marknodo = selnodo
						estado = Nodo_Sel
					if seledge != None:
						markedge = seledge
						estado = Edge_Sel

			if evento.type == pygame.KEYDOWN:
				if evento.key == pygame.K_s:
					grabar(nodos, edges, labels)
				if evento.key == pygame.K_q:
					sys.exit()
				if evento.key == pygame.K_ESCAPE:
					markedge = None
					marknodo = None
					estado = Nada
				if evento.key == pygame.K_n:
					estado = Crea_Nodo
					markedge = None
					marknodo = None
				if evento.key == pygame.K_e:
					if marknodo == None:
						mensaje = "Debe seleccionar primero un nodo de salida"
					else:
						estado = Crea_Edge
				if evento.key == pygame.K_r:
					if estado != Nada:
						if marknodo != None:
							for nodo in nodos:
								if marknodo == nodo:
									nodos.remove(nodo)
									toErase = []
									for edge in edges:
										if edge[0] == nodo or edge[1] == nodo:
											toErase.append(edge)
									for edge in toErase:
										edges.remove(edge)
									marknodo = None
						if markedge != None:
							for edge in edges:
								if markedge == edge:
									edges.remove(edge)
									markedge = None
					else:
						estado = Eliminando
						seledge = None
						selnodo = None
				if evento.key == pygame.K_l:
					mensaje = "Funcion aún no disponible"
					#agrega label (como hago???)
		
		screen.fill((255,255,255))
		for edge in edges:
			if edge != seledge:
				pygame.draw.aaline(screen, (0,0,0), edge[0], edge[1], 2)
		for nodo in nodos:
			#dibujar nodo
			pygame.draw.circle(screen, (0,0,0), nodo, 5, 5)
				
		#for label in labels:
			#escribir labelme.
		if seledge != None:
			pygame.draw.aaline(screen, (0,255,0), seledge[0], seledge[1], 4)
		if markedge != None:
			pygame.draw.aaline(screen, (255,0,0), markedge[0], markedge[1], 4)
		if selnodo != None:
			pygame.draw.circle(screen, (0,255,0), selnodo, 15, 3)
		if marknodo != None:
			pygame.draw.circle(screen, (255,0,0), marknodo, 15, 3)
		
		letras = pygame.font.Font(arial, 14).render(mensaje, 1, (0,0,0))
		screen.blit(letras, (0,0))
		letras = pygame.font.Font(arial, 14).render(str(estado), 1, (0,0,0))
		screen.blit(letras, (0,20))
		pygame.display.flip()
