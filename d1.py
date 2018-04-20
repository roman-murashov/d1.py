#!/usr/bin/env python

# Script and python library for interacting with Diablo 1 from Python.

import hook

# Hook into process.
p = hook.Process("djavul.exe")

# Global variable addresses and struct sizes.
players_addr = 0x686448
player_size = 0x54D8

def get_player(player_num=0):
	"""
	Return the contents of the given player struct.

	player_num -- player number in range [0, 4)
	"""
	check_player_num(player_num)
	addr = players_addr + player_size*player_num
	buf = p.read_mem(addr, player_size)
	return buf

def check_player_num(player_num):
	if not (0 <= player_num and player_num < 4):
		raise Exception("invalid player number; expected in range [0, 4), got {}".format(player_num))
