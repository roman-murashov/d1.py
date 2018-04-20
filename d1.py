#!/usr/bin/env python

# Script and python library for interacting with Diablo 1 from Python.

import hook

# Executable name.
exe_name = "djavul.exe"

# Global variable addresses and struct sizes.
players_addr = 0x686448
player_size = 0x54D8


def check_player_num(player_num):
	"""
	Validate player number.
	"""

	if not (0 <= player_num and player_num < 4):
		raise Exception("invalid player number; expected in range [0, 4), got {}".format(player_num))


def get_player(player_num=0):
	"""
	Return the contents of the given player struct.

	player_num -- player number in range [0, 4)
	"""

	with hook.Process(exe_name) as p:
		check_player_num(player_num)
		addr = players_addr + player_size*player_num
		buf = p.read_mem(addr, player_size)
		return bytearray(buf)


def set_player(player, player_num=0):
	"""
	Set the contents of the given player struct.

	player     -- contents of the player struct
	player_num -- player number in range [0, 4)
	"""

	with hook.Process(exe_name) as p:
		check_player_num(player_num)
		addr = players_addr + player_size*player_num
		buf = p.write_mem(addr, player)
		return buf
