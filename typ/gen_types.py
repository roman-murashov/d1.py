#!/usr/bin/env python2

import os
import cffi

def gen_types():
	dir = os.path.dirname(__file__)
	types_h_path = os.path.join(dir, "types.h.pre")
	with open(types_h_path) as f:
		ffi = cffi.FFI()
		ffi.cdef(f.read())
		ffi.set_source(
			"_types",
			'#include "types.h"',
		)
		ffi.compile()

if __name__ == '__main__':
	gen_types()
