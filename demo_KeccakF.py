#! /usr/bin/pythonw
# -*- coding: utf-8 -*-
# The Keccak sponge function, designed by Guido Bertoni, Joan Daemen,
# Michaël Peeters and Gilles Van Assche. For more information, feedback or
# questions, please refer to our website: http://keccak.noekeon.org/
# 
# Implementation by Renaud Bauvin,
# hereby denoted as "the implementer".
# 
# To the extent possible under law, the implementer has waived all copyright
# and related or neighboring rights to the source code in this file.
# http://creativecommons.org/publicdomain/zero/1.0/

import KeccakSponge

A=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]

myKeccak=KeccakSponge.KeccakSponge(1600)

myKeccak.KeccakF(A, True)

# TODO util probably shouldn't be visible from here
myKeccak.util.printState(A,'Final result')
