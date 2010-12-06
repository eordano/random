# -*- coding: utf-8 -*-
import pygame, sys, os

def vecino(pos):
	d = [(0,1),(1,0),(0,-1),(-1,0)]
	for i in range(4):
		if pos[0]+d[i][0] < 0 or pos[0]+d[i][0] > 18:
			yield (pos)
		elif pos[1]+d[i][1] < 0 or pos[1]+d[i][1] > 18:
			yield (pos)
		else:
			yield (pos[0]+d[i][0], pos[1]+d[i][1])

def coor_from_point(pos):
	return (int((pos[0]-4)/31.2), int((pos[1]-4)/31.2))

def point_from_coor(pos):
	return (int(pos[0]*31.2+4), int(pos[1]*31.2+4))

def bfs(x, y, l):
	queue = [(x,y)]
	seen = set(queue)
	index = 0
	liberties = 0
	while len(queue)-index > 0:
		elem = queue[index]
		index += 1
		for vec in vecino(elem):
			if vec not in seen:
				seen.add(vec)
				if l[vec[0]][vec[1]] == 0:
					liberties += 1
				elif l[vec[0]][vec[1]] == l[x][y]:
					queue.append(vec)
	return (queue, liberties)

if __name__ == '__main__':
	screen = pygame.display.set_mode((600,600))
	l = [[0 for i in range(19)] for j in range(19)]
	turno = 2
	ko = None
	tablero = pygame.image.load('tablero.png')
	blancas = pygame.image.load('blancas.png')
	negras = pygame.image.load('negras.png')
	
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
				cx, cy = coor_from_point(pygame.mouse.get_pos())
				if cx >= 0 and cy >= 0 and cx < 19 and cy < 19 and l[cx][cy] == 0:
					puede = False
					l[cx][cy] = turno
					for vec in vecino((cx,cy)):
						if l[vec[0]][vec[1]] == (l[cx][cy]%2)+1:
							res = bfs(vec[0],vec[1],l)
							if res[1] == 0:
								puede = True
					if bfs(cx,cy,l)[1] > 0:
						puede = True
					if ko == (cx,cy):
						puede = False
					l[cx][cy] = 0
					if puede:
						ko = None
						l[cx][cy] = turno
						for vec in vecino((cx,cy)):
							if l[vec[0]][vec[1]] == (l[cx][cy]%2)+1:
								res = bfs(vec[0], vec[1],l)
								if res[1] == 0:
									for pos in res[0]:
										l[pos[0]][pos[1]] = 0
									if len(res[0]) == 1 and bfs(cx,cy,l)[1] == 1:
										ko = res[0][0]
						turno = (turno)%2+1
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					sys.exit()
				if event.key == pygame.K_n and pygame.key.get_mods() & pygame.KMOD_LSHIFT:
					l = [[0 for i in range(19)] for j in range(19)]
					turno = 1
			if event.type == pygame.QUIT:
				sys.exit()
		screen.fill((0,0,0))
		screen.blit(tablero, (0,0))
		for i in range(19):
			for j in range(19):
				if l[i][j] == 1:
					screen.blit(blancas, point_from_coor((i,j)))
				if l[i][j] == 2:
					screen.blit(negras, point_from_coor((i,j)))
		if ko != None:
			pygame.draw.rect(screen, (255,255,255), (point_from_coor(ko), (15, 15)), 3)
		pygame.display.flip()
