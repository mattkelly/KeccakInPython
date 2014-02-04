#! /usr/bin/pythonw
# -*- coding: utf-8 -*-
# The Keccak sponge function, designed by Guido Bertoni, Joan Daemen,
# Michaël Peeters and Gilles Van Assche. For more information, feedback or
# questions, please refer to our website: http://keccak.noekeon.org/
# 
# Implementation by Renaud Bauvin and Matt Kelly,
# hereby denoted as "the implementer".
# 
# To the extent possible under law, the implementer has waived all copyright
# and related or neighboring rights to the source code in this file.
# http://creativecommons.org/publicdomain/zero/1.0/

import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../KeccakF')
import KeccakF

A = [[0] * 5 for i in range(5)]

KeccakF.KeccakF(A, w=64, nr=24, verbose=True)

KeccakF.printState(A, 'Final result')

