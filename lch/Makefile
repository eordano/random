# Makefile for Lightweight C Httpserver (LCH)

FILES=init_lch request_marshall dlinked_list lch_helpers

CC=gcc
CFLAGS=-O2 -Wall -g
LIBS=

# Dirs
SRCDIR=src
OBJDIR=build

all: $(OBJDIR) $(patsubst %,$(OBJDIR)/%.o,$(FILES))
	ld -o lch.o $(patsubst %,$(OBJDIR)/%.o,$(FILES)) -lc

$(OBJDIR)/%.o: $(SRCDIR)/%.c
	$(CC) $(CFLAGS) $(LIBS) -c $(SRCDIR)/`basename $@ .o`.c -o $@

$(OBJDIR):
	mkdir $(OBJDIR)

clean :
	rm -rf $(OBJDIR)
	rm -f *.o

