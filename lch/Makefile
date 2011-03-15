#
#
# Makefile for Lightweight C Httpserver (LCH)
#
#

CC=gcc
OBJECTS=server.o request_marshall.o dlinked_list.o application.o
CFLAGS=-O2 -Wall
LIBS=

lch: $(OBJECTS) 
	$(CC) $(CFLAGS) $(LIBS) -o lch $(OBJECTS) 

server.o: server.c
	$(CC) $(CFLAGS) $(LIBS) -c server.c 

request_marshall.o: marshall/request_marshall.c marshall/request_marshall.h 
	$(CC) $(CFLAGS) $(LIBS) -c marshall/request_marshall.c

dlinked_list.o: util/dlinked_list.c util/dlinked_list.h
	$(CC) $(CFLAGS) $(LIBS) -c util/dlinked_list.c

application.o: application/application.c application/application.h
	$(CC) $(CFLAGS) $(LIBS) -c application/application.c

clean :
	rm -f lch *.o
