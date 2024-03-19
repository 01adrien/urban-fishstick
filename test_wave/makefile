FLAGS := -I. -g3  # -std=c99
BIN := build

run: $(BIN)
	@ ./$(BIN)

$(BIN): main.c
	@ gcc $(FLAGS) -o $@ $^ -lm

valgrind:                                                                       
	@ valgrind --leak-check=full --show-leak-kinds=all ./$(BIN) index.lox

clean:
	@ rm -f $(BIN) gc

