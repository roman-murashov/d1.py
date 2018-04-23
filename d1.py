#!/usr/bin/env python2

# Script and python library for interacting with Diablo 1 from Python.

from io import BytesIO
from typ._types import ffi
from typ._types import lib as types
import hook
import logging

# Enable debug output.
logging.basicConfig(level=logging.DEBUG)

# Executable name.
djavul_exe_name = "djavul.exe"

# Global variable addresses and struct sizes.
players_addr = 0x686448
player_size = 0x54D8

# Process being debugged.
process = None

def init_hook():
	'''
	Initialize the debugger and attach it to the djavul.exe process.
	'''
	global process
	process = hook.Process(djavul_exe_name)


# Initialize a debugger for the process, if djavul.exe is present.
if hook.find_pid(djavul_exe_name):
	init_hook()


def get_player(player_num=0):
	'''
	Return the given player struct.

	player_num -- player number in range [0, 4)
	'''

	player_buf = get_player_content(player_num)
	player = ffi.new('Player *')
	stream = BytesIO(player_buf)
	stream.readinto(ffi.buffer(player))
	return player


def set_player(player, player_num=0):
	'''
	Set the given player struct.

	player     -- contents of the player struct
	player_num -- player number in range [0, 4)
	'''

	player_buf = ffi.buffer(player)[:]
	set_player_content(player_buf, player_num)


def get_player_content(player_num=0):
	'''
	Return the contents of the given player struct.

	player_num -- player number in range [0, 4)
	'''
	assert 0 <= player_num < 4

	addr = players_addr + player_size*player_num
	buf = process.read_mem(addr, player_size)
	return bytearray(buf)


def set_player_content(player_buf, player_num=0):
	'''
	Set the contents of the given player struct.

	player     -- contents of the player struct
	player_num -- player number in range [0, 4)
	'''
	assert len(player_buf) == player_size
	assert 0 <= player_num < 4

	addr = players_addr + player_size*player_num
	process.write_mem(addr, player_buf)
