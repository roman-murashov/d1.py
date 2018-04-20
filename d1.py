#!/usr/bin/env python

# Script and python library for interacting with Diablo 1 from Python.

import hook

# Executable name.
djavul_exe_name = "djavul.exe"

# Global variable addresses and struct sizes.
players_addr = 0x686448
player_size = 0x54D8


def get_player(player_num=0):
	'''
	Return the contents of the given player struct.

	player_num -- player number in range [0, 4)
	'''
	assert 0 <= player_num < 4

	with hook.Process(djavul_exe_name) as p:
		addr = players_addr + player_size*player_num
		buf = p.read_mem(addr, player_size)
		return bytearray(buf)


def set_player(player, player_num=0):
	'''
	Set the contents of the given player struct.

	player     -- contents of the player struct
	player_num -- player number in range [0, 4)
	'''
	assert len(player) == player_size
	assert 0 <= player_num < 4

	with hook.Process(djavul_exe_name) as p:
		addr = players_addr + player_size*player_num
		buf = p.write_mem(addr, player)
		return buf
