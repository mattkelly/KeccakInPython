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

# Constants

## Round constants
RC=[0x0000000000000001,
    0x0000000000008082,
    0x800000000000808A,
    0x8000000080008000,
    0x000000000000808B,
    0x0000000080000001,
    0x8000000080008081,
    0x8000000000008009,
    0x000000000000008A,
    0x0000000000000088,
    0x0000000080008009,
    0x000000008000000A,
    0x000000008000808B,
    0x800000000000008B,
    0x8000000000008089,
    0x8000000000008003,
    0x8000000000008002,
    0x8000000000000080,
    0x000000000000800A,
    0x800000008000000A,
    0x8000000080008081,
    0x8000000000008080,
    0x0000000080000001,
    0x8000000080008008]

## Rotation offsets
r=[[ 0, 36,  3, 41, 18],
   [ 1, 44, 10, 45,  2],
   [62,  6, 43, 15, 61],
   [28, 55, 25, 21, 56],
   [27, 20, 39,  8, 14]]

## Generic utility functions

def rot(x,n,w):
    """Bitwise rotation (to the left) of n bits considering the \
    string of bits is w bits long"""

    n = n % w
    return ((x>>(w-n))+(x<<n))%(1<<w)

def printState(state, info):
    """Print on screen the state of the sponge function preceded by \
    string info

    state: state of the sponge function
    info: a string of characters used as identifier"""

    print("Current value of state: %s" % (info))
    for y in range(5):
        line=[]
        for x in range(5):
             line.append(hex(state[x][y]))
        print('\t%s' % line)

def Round(A, w, RCfixed):
    """Perform one round of computation as defined in the Keccak-f permutation

    A: current state (5×5 matrix)
    RCfixed: value of round constant to use (integer)
    """

    #Initialisation of temporary variables
    B = [[0] * 5 for i in range(5)]
    C = [0] * 5
    D = [0] * 5

    #Theta step
    for x in range(5):
        C[x] = A[x][0]^A[x][1]^A[x][2]^A[x][3]^A[x][4]

    for x in range(5):
        D[x] = C[(x-1)%5]^rot(C[(x+1)%5], 1, w)

    for x in range(5):
        for y in range(5):
            A[x][y] = A[x][y]^D[x]

    #Rho and Pi steps
    for x in range(5):
      for y in range(5):
            B[y][(2*x+3*y)%5] = rot(A[x][y], r[x][y], w)

    #Chi step
    for x in range(5):
        for y in range(5):
            A[x][y] = B[x][y]^((~B[(x+1)%5][y]) & B[(x+2)%5][y])

    #Iota step
    A[0][0] = A[0][0]^RCfixed

    return A

def KeccakF(A, w, nr, verbose=False):
    """Perform Keccak-f function on the state A

    A: 5×5 matrix containing the state
    verbose: a boolean flag activating the printing of intermediate computations
    """

    if verbose:
        printState(A,"Before first round")

    for i in range(nr):
        #NB: result is truncated to lane size
        A = Round(A, w, RC[i]%(1<<w))

        if verbose:
              printState(A,"Status end of round #%d/%d" % (i+1, nr))

    return A

