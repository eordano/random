# -*- coding: utf-8 -*-
import sys

if __name__ == '__main__':
    Infty = -1
    archivo = sys.stdin
    N, M = [int(a) for a in archivo.readline().split()]
    edges = dict([(a,[]) for a in range(N)])
    for variable in range(M):
        a, b = [int(r) for r in archivo.readline().split()]
        edges[a].append(b)
    seen = set([0])
    distance = [Infty for a in range(N)]
    distance[0] = 0
    queue = [0]
    while len(queue):
        n = queue[0]
        queue = queue[1:]
        for m in edges[n]:
            if m not in seen:
                distance[m] = distance[n]+1
                seen.add(m)
                queue.append(m)
    for i in range(N):
        print "distancia a", i, "es", distance[i]
