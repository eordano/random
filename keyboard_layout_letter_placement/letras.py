# -*- coding: utf-8 -*-
import pygame, sys

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    cajas = []
    arial = pygame.font.match_font('arial')
    background = pygame.image.load('blank1.gif')
    screen = pygame.display.set_mode(background.get_size())
    archivo = sys.stdin
    for line in archivo:
        letra, frecuencia = line.split()
        not_done = True
        image = pygame.Surface((30,30))
        image.fill((0,255,0))
        image.blit(pygame.font.Font(arial, 24).render(letra, 1, (0,0,0)), (0,0))
        selecc = pygame.Surface((30,30))
        selecc.fill((255,0,0))
        selecc.blit(pygame.font.Font(arial, 14).render(letra, 1, (0,0,0)), (0,0))
        
        while not_done:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    not_done = False
                    donde = pygame.mouse.get_pos()
                    cajas.append({'imagen': image,
                                  'freq': float(frecuencia),
                                  'pos': (donde[0]-15, donde[1]-15),
                                  'letra': letra,
                                  'selec': selecc })
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        sys.exit()
            screen.fill((255,255,255))
            donde = pygame.mouse.get_pos()
            screen.blit(background, (0,0))
            screen.blit(image, (donde[0]-15, donde[1]-15))
            for caja in cajas:
                screen.blit(caja['imagen'], caja['pos'])
            pygame.display.flip()
    
    seleccionados = []
    total = sum(caja['freq'] for caja in cajas)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                donde = pygame.mouse.get_pos()
                no_seleccione = True
                for caja in cajas:
                    if donde[0] > caja['pos'][0] and donde[1] > caja['pos'][1]:
                        if donde[0] < caja['pos'][0]+30 and donde[1] < caja['pos'][1]+30:
                            if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                                if not caja in seleccionados:
                                    seleccionados.append(caja)
                            else:
                                seleccionados = [caja]
                            no_seleccione = False
                if no_seleccione:
                    seleccionados = []
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_ESCAPE:
                    seleccionados = []
            if event.type == pygame.MOUSEMOTION:
                if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                    if pygame.mouse.get_pressed()[0]:
                        for caja in seleccionados:
                            caja['pos'] = (caja['pos'][0]+event.rel[0], caja['pos'][1]+event.rel[1])

        screen.fill((255,255,255))
        screen.blit(background, (0,0)) 
        for caja in cajas:
            if caja in seleccionados:
                screen.blit(caja['selec'], caja['pos'])
            else:
                screen.blit(caja['imagen'], caja['pos'])
        
        suma = sum(caja['freq'] for caja in seleccionados)
        screen.blit(pygame.font.Font(arial, 14).render('%d/%d = %g'%(suma, total, float(suma)/total), 1, (255,255,255), (0,0,0)), (0,0))
        pygame.display.flip()
