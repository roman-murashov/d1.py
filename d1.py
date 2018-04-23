#!/usr/bin/env python2

# Script and python library for interacting with Diablo 1 from Python.

from io import BytesIO

import hook
from typ._types import ffi
from typ._types import lib as types

# Executable name.
djavul_exe_name = "djavul.exe"

# Global variable addresses and struct sizes.
players_addr = 0x686448
player_size = 0x54D8


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

	with hook.Process(djavul_exe_name) as p:
		addr = players_addr + player_size*player_num
		buf = p.read_mem(addr, player_size)
		return bytearray(buf)


def set_player_content(player_buf, player_num=0):
	'''
	Set the contents of the given player struct.

	player     -- contents of the player struct
	player_num -- player number in range [0, 4)
	'''
	assert len(player_buf) == player_size
	assert 0 <= player_num < 4

	with hook.Process(djavul_exe_name) as p:
		addr = players_addr + player_size*player_num
		p.write_mem(addr, player_buf)
