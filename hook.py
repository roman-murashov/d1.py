#!/usr/bin/env python2

# Process hooking functions.

# TODO: update to Python 3 when lldb supports Python 3.
import lldb
import psutil
import logging


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
	# Debugger
	dbg = None
	# Handle to the process.
	process = None
	# lldb command prompt.
	prompt = None
	# Executable name.
	exe_name = ""
	# Process ID.
	pid = 0

	def __init__(self, exe_name="", pid=0):
		'''
		Hook into the process.

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
		logging.debug("hooking into process {} with PID {}\n".format(self.exe_name, self.pid))
		self.dbg = lldb.SBDebugger.Create()
		self.prompt = self.dbg.GetCommandInterpreter()
		target = self.dbg.CreateTarget('')
		listener = self.dbg.GetListener()
		error = lldb.SBError()
		self.process = target.AttachToProcessWithID(listener, self.pid, error)
		if not error.Success():
			raise Exception("unable to attach to process {}; {}".format(self.pid, error.GetCString()))
		assert self.process.GetProcessID() != lldb.LLDB_INVALID_PROCESS_ID


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
		Unhook the process from the debugger.
		'''

		if self.process:
			logging.debug("unhooking from process {} with PID {}\n".format(self.exe_name, self.pid))
			self.process.Detach()
			self.process = None
		if self.dbg:
			self.dbg.Terminate()
			self.dbg = None


	def run_cmd(self, command):
		'''
		Run command in lldb prompt.

		command -- lldb command
		'''

		ret = lldb.SBCommandReturnObject()
		self.prompt.HandleCommand(command, ret)
		if ret.Succeeded():
			print(ret.GetOutput())
		else:
			print(ret)


	def read_mem(self, start, n):
		'''
		Read the memory region [start, start+n) of the process.

		start -- start address
		n     -- number of bytes to read
		'''

		output_path = '/tmp/out_%d.bin' % (self.pid)
		self.run_cmd('memory read --force -b -o %s 0x%08X 0x%08X' % (output_path, start, start+n))
		# TODO: add error handling for open
		with open(output_path, 'rb') as f:
			return f.read()


	def write_mem(self, addr, buf):
		'''
		Write the buffer to the specified address of the process.

		start -- start address
		n     -- number of bytes to read
		'''

		print(buf)
		input_path = '/tmp/in_%d.bin' % (self.pid)
		# TODO: add error handling for open
		with open(input_path, 'wb') as f:
			f.write(buf)
			f.flush()
		self.run_cmd('memory write -i %s 0x%08X' % (input_path, addr))
