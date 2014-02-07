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

import KeccakUtil

class KeccakDuplex:
    """
    Class implementing the Keccak duplex construction
    """
    def __init__(self, b = 1600, r = 1024, c = 576):
        """Constructor:

        b: parameter b, must be 25, 50, 100, 200, 400, 800 or 1600 (default value)"""
        self.setB(b)
        self.util = KeccakUtil.KeccakUtil(b, r)
        self.r = r 
        self.c = c

        # Duplex objects do maintain state - initialize it here
        self.S = [[0] * 5 for i in range(5)]
        print S

    def setB(self, b):
        """Set the value of the parameter b (and thus w,l and nr)

        b: parameter b, must be choosen among [25, 50, 100, 200, 400, 800, 1600]
        """

        if b not in [25, 50, 100, 200, 400, 800, 1600]:
            raise KeccakError.KeccakError('b value not supported - use 25, 50, 100, 200, 400, 800 or 1600')

        # Update all the parameters based on the used value of b
        self.b=b
        self.w=b//25
        self.l=int(math.log(self.w,2))
        self.nr=12+2*self.l

    def Round(self, A, RCfixed):
        """Perform one round of computation as defined in the Keccak-f permutation

        A: current state (5×5 matrix)
        RCfixed: value of round constant to use (integer)
        """

        #Initialisation of temporary variables
        B=[[0,0,0,0,0],
           [0,0,0,0,0],
           [0,0,0,0,0],
           [0,0,0,0,0],
           [0,0,0,0,0]]
        C= [0,0,0,0,0]
        D= [0,0,0,0,0]

        #Theta step
        for x in range(5):
            C[x] = A[x][0]^A[x][1]^A[x][2]^A[x][3]^A[x][4]

        for x in range(5):
            D[x] = C[(x-1)%5]^self.util.rot(C[(x+1)%5],1)

        for x in range(5):
            for y in range(5):
                A[x][y] = A[x][y]^D[x]

        #Rho and Pi steps
        for x in range(5):
          for y in range(5):
                B[y][(2*x+3*y)%5] = self.util.rot(A[x][y], self.util.r[x][y])

        #Chi step
        for x in range(5):
            for y in range(5):
                A[x][y] = B[x][y]^((~B[(x+1)%5][y]) & B[(x+2)%5][y])

        #Iota step
        A[0][0] = A[0][0]^RCfixed

        return A

    def KeccakF(self, A, verbose=False):
        """Perform Keccak-f function on the state A

        A: 5×5 matrix containing the state
        verbose: a boolean flag activating the printing of intermediate computations
        """

        if verbose:
            self.util.printState(A, "Before first round")

        for i in range(self.nr):
            #NB: result is truncated to lane size
            A = self.Round(A, self.util.RC[i]%(1<<self.w))

            if verbose:
                  self.util.printState(A, "Status end of round #%d/%d" % (i+1,self.nr))

        return A

    def duplexing(sigma, outLen):
      pass
