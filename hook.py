#!/usr/bin/env python2

# Process hooking functions.

# TODO: update to Python 3 when LLDB supports Python 3.
import lldb
import logging
import psutil


def find_pid(exe_name):
	'''
	Locate the process ID of the executable.

	exe_name -- executable name.
	'''

	for p in psutil.process_iter():
		if p.name() == exe_name:
			return p.pid
	return None


def find_exe_name(pid):
	'''
	Locate the name of the executable with the given process ID.

	pid -- process ID
	'''

	for p in psutil.process_iter():
		if p.pid == pid:
			return p.name()
	return None


class Process:
	'''
	Process interaction through the hooks of a debugger.
	'''

	# Debugger.
	dbg = None
	# LLDB command interpreter (command prompt).
	ci = None
	# Executable name.
	exe_name = ""
	# Process ID.
	pid = 0


	def __init__(self, exe_name="", pid=0):
		'''
		Create a debugger for the process. Specify at least one of exe_name and
		pid.

		exe_name -- executable name (optional)
		pid      -- process ID (optional)
		'''
		assert exe_name or pid

		self.exe_name = exe_name
		self.pid = pid
		# Locate executable name from PID.
		if not exe_name:
			self.exe_name = find_exe_name(self.pid)
			if not self.exe_name:
				raise Exception("unable to locate executable name of process with PID {}".format(self.pid))

		# Locate PID from executable name.
		if not self.pid:
			self.pid = find_pid(self.exe_name)
			if not self.pid:
				raise Exception("unable to locate PID of executable {}".format(self.exe_name))

		# Initialize debugger and attach process.
		logging.debug("create debugger for process {} with PID {}\n".format(self.exe_name, self.pid))
		self.dbg = lldb.SBDebugger.Create()
		self.ci = self.dbg.GetCommandInterpreter()


	def __enter__(self):
		'''
		Implement `with` interface.
		'''

		return self


	def __exit__(self, type, value, traceback):
		'''
		Implement `with` interface.
		'''

		self.__del__()


	def __del__(self):
		'''
		Terminate the debugger of the process.
		'''

		if self.dbg:
			logging.debug("terminate debugger of process {} with PID {}\n".format(self.exe_name, self.pid))
			self.dbg.Terminate()
			self.dbg = None


	def run_cmd(self, cmd, output=False):
		'''
		Run command in LLDB command interpreter (command prompt).

		cmd -- LLDB command
		'''

		ret = lldb.SBCommandReturnObject()
		self.ci.HandleCommand(cmd, ret)
		if output:
			if ret.Succeeded():
				print(ret.GetOutput())
			else:
				print(ret)


	def attach(self):
		'''
		attach to the process.
		'''

		self.run_cmd('attach {}'.format(self.pid))


	def detach(self):
		'''
		detach from the process.
		'''

		self.run_cmd('detach')


	def read_mem(self, start, n):
		'''
		Read the memory region [start, start+n) of the process.

		start -- start address
		n     -- number of bytes to read
		'''

		output_path = '/tmp/out_{}.bin'.format(self.pid)
		self.attach()
		self.run_cmd('memory read --force -b -o %s 0x%08X 0x%08X' % (output_path, start, start+n))
		self.detach()
		# TODO: add error handling for open
		with open(output_path, 'rb') as f:
			return f.read()


	def write_mem(self, addr, buf):
		'''
		Write the buffer to the specified address of the process.

		start -- start address
		n     -- number of bytes to read
		'''

		input_path = '/tmp/in_{}.bin'.format(self.pid)
		# TODO: add error handling for open
		with open(input_path, 'wb') as f:
			f.write(buf)
			f.flush()
		self.attach()
		self.run_cmd('memory write -i %s 0x%08X' % (input_path, addr))
		self.detach()
