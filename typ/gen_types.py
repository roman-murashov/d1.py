#!/usr/bin/env python2

import cffi
import os

def get_sources():
	sources = []
	for dir in ['notes/rdata', 'notes/data', 'notes/bss']:
		sources += [os.path.join(dir, x) for x in os.listdir(dir) if x.endswith('.h')]
	return sources

def file_get_content(path):
	return open(path).read()

def gen_types():
	ffi = cffi.FFI()

	# Parse types.h
	dir = os.path.dirname(__file__)
	types_h_path = os.path.join(dir, 'notes/include/types.h.pre')
	types_h_buf = file_get_content(types_h_path)
	ffi.cdef(types_h_buf)
	sources_buf = '#include "types.h"\n'

	# Parse rdata, data and bss .h files
	for path in get_sources():
		buf = file_get_content(path)
		ffi.cdef(buf)
		sources_buf += '#include "{}"\n'.format(path)
	ffi.set_source(
		'_types',
		sources_buf,
		include_dirs=['notes/include'],
	)
	ffi.compile()

if __name__ == '__main__':
	gen_types()
