all: _types.cpython-36m-x86_64-linux-gnu.so clean

notes_repo=~/Desktop/go/src/github.com/sanctuary/notes

types.h:
	cp ${notes_repo}/enums.h .
	cp ${notes_repo}/sha1.h .
	cp ${notes_repo}/structs.h .
	cp ${notes_repo}/typedefs.h .
	cp ${notes_repo}/types.h .
	cp ${notes_repo}/windows.h .
	sar -i "#include <stdarg.h>\n" "" typedefs.h
	sar -i "uint16_t blocks[[]nblocks[]];" "uint16_t blocks[10];" structs.h

types.h.pre: types.h
	gcc -E -o $@ $^

_types.cpython-36m-x86_64-linux-gnu.so: types.h.pre
	./gen_types.py

clean:
	rm -f types.h.pre _types.c *.o
	rm -f enums.h
	rm -f sha1.h
	rm -f structs.h
	rm -f typedefs.h
	rm -f types.h
	rm -f windows.h

.PHONY:
	clean
