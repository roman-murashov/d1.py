#!/usr/bin/env python2

# Script and python library for interacting with Diablo 1 from Python.

from io import BytesIO
from typ._types import ffi, lib
import hook
import logging

# Enable debug output.
logging.basicConfig(level=logging.DEBUG)

# Executable name.
djavul_exe_name = "djavul.exe"

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


def set_data(addr, data):
	'''
	Store data to the memory region [addr, addr+len(data)).
	'''

	process.write_mem(addr, data)


def get_data(addr, n):
	'''
	Return the contents of the memory region [addr, addr+n).
	'''

	return process.read_mem(addr, n)


def get_elem_addr(start, size, i, n):
	'''
	Return the address of the i:th element in the array of n elements with the
	given start address and element size.
	'''
	assert 0 <= i and i < n

	return start + i*size


# players
players_addr = 0x686448
players_n = ffi.typeof(lib.players).length
player_size = ffi.sizeof(ffi.typeof(lib.players[0]))


def set_player(player, player_num=0):
	'''
	Set the given player struct.

	player     -- contents of the player struct
	player_num -- player number in range [0, 4)
	'''
	if ffi.typeof(player) == ffi.typeof('Player'):
		# Convert 'Player' to 'Player *'
		player = ffi.addressof(player)
	assert ffi.typeof(player) == ffi.typeof('Player *')
	assert 0 <= player_num and player_num < players_n

	player_buf = ffi.buffer(player)[:]
	addr = get_elem_addr(players_addr, player_size, player_num, players_n)
	set_data(addr, player_buf)


def get_player(player_num=0):
	'''
	Return the given player struct.

	player_num -- player number in range [0, 4)
	'''
	assert 0 <= player_num and player_num < players_n

	addr = get_elem_addr(players_addr, player_size, player_num, players_n)
	player_buf = get_data(addr, player_size)
	player = ffi.new('Player *')
	stream = BytesIO(player_buf)
	stream.readinto(ffi.buffer(player))
	return player


# items
items_addr = 0x635A28
items_n = ffi.typeof(lib.items).length
item_size = ffi.sizeof(ffi.typeof(lib.items[0]))


def set_item(item, item_num=0):
	'''
	Set the given item struct.

	item     -- contents of the item struct
	item_num -- item number in range [0, 4)
	'''
	if ffi.typeof(item) == ffi.typeof('Item'):
		# Convert 'Item' to 'Item *'
		item = ffi.addressof(item)
	assert ffi.typeof(item) == ffi.typeof('Item *')
	assert 0 <= item_num and item_num < items_n

	item_buf = ffi.buffer(item)[:]
	addr = get_elem_addr(items_addr, item_size, item_num, items_n)
	set_data(addr, item_buf)


def get_item(item_num=0):
	'''
	Return the given item struct.

	item_num -- item number in range [0, 4)
	'''
	assert 0 <= item_num and item_num < items_n

	addr = get_elem_addr(items_addr, item_size, item_num, items_n)
	item_buf = get_data(addr, item_size)
	item = ffi.new('Item *')
	stream = BytesIO(item_buf)
	stream.readinto(ffi.buffer(item))
	return item
