#
#
# Makefile for Lightweight C Httpserver (LCH)
#
#

CC=gcc
OBJECTS=init_lch.o request_marshall.o dlinked_list.o lch_helpers.o
CFLAGS=-O2 -Wall -g
LIBS=

lch: $(OBJECTS) 
	ld -o lch.o $(OBJECTS) -lc
	rm -f init_lch.o request_marshall.o dlinked_list.o lch_helpers.o

init_lch.o: src/init_lch.c include/lch.h
	$(CC) $(CFLAGS) $(LIBS) -c src/init_lch.c 

request_marshall.o: src/request_marshall.c src/include/request_marshall.h 
	$(CC) $(CFLAGS) $(LIBS) -c src/request_marshall.c

dlinked_list.o: src/dlinked_list.c include/dlinked_list.h
	$(CC) $(CFLAGS) $(LIBS) -c src/dlinked_list.c

lch_helpers.o: src/lch_helpers.c
	$(CC) $(CFLAGS) $(LIBS) -c src/lch_helpers.c

clean :
	rm -f init_lch.o request_marshall.o dlinked_list.o lch_helpers.o lch.o
