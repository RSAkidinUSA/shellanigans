CC = gcc
SRC := inc.c
BIN = inc
.PHONY: clean

all: 
	@echo "Invalid use of make, please use one of the given options"

build: $(SRC)
	$(CC) $^ -o $(BIN) -w

clean:
	$(eval rm-ignore = $(foreach file, $(SRC),-not -name $(file)))
	@find . -type f $(rm-ignore) -not -name Makefile -delete