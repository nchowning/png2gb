BIN=../gbdk-n/bin
OBJ=./obj

all: generate build

generate:
	./png2gb.py yesimnathan.png

build:
	mkdir -p $(OBJ)
	$(BIN)/gbdk-n-compile.sh main.c -o $(OBJ)/main.rel
	$(BIN)/gbdk-n-link.sh $(OBJ)/main.rel -o $(OBJ)/main.ihx
	$(BIN)/gbdk-n-make-rom.sh $(OBJ)/main.ihx yesimnathan.gb

clean:
	rm -rf $(OBJ) map.c tiles.c yesimnathan.gb yesimnathan.sav

.PHONY: all generate clean
