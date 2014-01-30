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

import sys, os, math
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../KeccakF')
import KeccakF

class KeccakError(Exception):
    """
    Class of error used in the Keccak implementation

    Use: raise KeccakError.KeccakError("Text to be displayed")
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class KeccakSponge:
    """
    Class implementing the Keccak sponge function
    """

    def __init__(self, r=1024, c=576, n=1024, verbose=False):
        """
        Constructor:

        r: bitrate in bits (defautl: 1024)
        c: capacity in bits (default: 576)
        n: length of output in bits (default: 1024),
        verbose: print the details of computations(default:False)
        """

        self.r = r
        self.c = c
        self.b = r + c
        self.n = n
        self.w = self.b // 25
        self.l = int(math.log(self.w, 2))
        self.nr = 12 + 2 * self.l
        self.verbose = verbose

        #Check the inputs
        if self.b not in [25, 50, 100, 200, 400, 800, 1600]:
           raise KeccakError.KeccakError('b value not supported - use 25, 50, 100, 200, 400, 800 or 1600')
        if (self.r<0) or (self.r%8!=0):
            raise KeccakError.KeccakError('r must be a multiple of 8 in this implementation')
        if (self.n%8!=0):
            raise KeccakError.KeccakError('outputLength must be a multiple of 8')

        if self.verbose:
            print("Create a Keccak function with (r=%d, c=%d (i.e. w=%d))" % (
              self.r, self.c, self.w))
 
        # Initialisation of state
        self.S=[[0,0,0,0,0],
               [0,0,0,0,0],
               [0,0,0,0,0],
               [0,0,0,0,0],
               [0,0,0,0,0]]

    ### Padding rule

    def pad10star1(self, M, n):
        """
        Pad M with the pad10*1 padding rule to reach a length multiple of r bits

        M: message pair (length in bits, string of hex characters ('9AFC...')
        n: length in bits (must be a multiple of 8)
        Example: pad10star1([60, 'BA594E0FB9EBBD30'],8) returns 'BA594E0FB9EBBD93'
        """

        [my_string_length, my_string]=M

        # Check the parameter n
        if n%8!=0:
            raise KeccakError.KeccakError("n must be a multiple of 8")

        # Check the length of the provided string
        if len(my_string)%2!=0:
            #Pad with one '0' to reach correct length (don't know test
            #vectors coding)
            my_string=my_string+'0'
        if my_string_length>(len(my_string)//2*8):
            raise KeccakError.KeccakError("the string is too short to contain the number of bits announced")

        nr_bytes_filled=my_string_length//8
        nbr_bits_filled=my_string_length%8
        l = my_string_length % n
        if ((n-8) <= l <= (n-2)):
            if (nbr_bits_filled == 0):
                my_byte = 0
            else:
                my_byte=int(my_string[nr_bytes_filled*2:nr_bytes_filled*2+2],16)
            my_byte=(my_byte>>(8-nbr_bits_filled))
            my_byte=my_byte+2**(nbr_bits_filled)+2**7
            my_byte="%02X" % my_byte
            my_string=my_string[0:nr_bytes_filled*2]+my_byte
        else:
            if (nbr_bits_filled == 0):
                my_byte = 0
            else:
                my_byte=int(my_string[nr_bytes_filled*2:nr_bytes_filled*2+2],16)
            my_byte=(my_byte>>(8-nbr_bits_filled))
            my_byte=my_byte+2**(nbr_bits_filled)
            my_byte="%02X" % my_byte
            my_string=my_string[0:nr_bytes_filled*2]+my_byte
            while((8*len(my_string)//2)%n < (n-8)):
                my_string=my_string+'00'
            my_string = my_string+'80'

        return my_string

    def fromHexStringToLane(self, string):
        """
        Convert a string of bytes written in hexadecimal to a lane value
        """

        #Check that the string has an even number of characters i.e. whole number of bytes
        if len(string)%2!=0:
            raise KeccakError.KeccakError("The provided string does not end with a full byte")

        #Perform the modification
        temp=''
        nrBytes=len(string)//2
        for i in range(nrBytes):
            offset=(nrBytes-i-1)*2
            temp+=string[offset:offset+2]
        return int(temp, 16)

    def fromLaneToHexString(self, lane):
        """ 
        Convert a lane value to a string of bytes written in hexadecimal
        """

        laneHexBE = (("%%0%dX" % (self.w//4)) % lane)
        #Perform the modification
        temp=''
        nrBytes=len(laneHexBE)//2
        for i in range(nrBytes):
            offset=(nrBytes-i-1)*2
            temp+=laneHexBE[offset:offset+2]
        return temp.upper()

    ### Conversion functions String <-> Table (and vice-versa)

    def convertStrToTable(self, string):
        """
        Convert a string of bytes to its 5×5 matrix representation

        string: string of bytes of hex-coded bytes (e.g. '9A2C...')
        """

        #Check that input paramaters
        if self.w%8!= 0:
            raise KeccakError("w is not a multiple of 8")
        if len(string)!=2*(self.b)//8:
            raise KeccakError.KeccakError("String can't be divided in 25 blocks of w bits\
            i.e. string must have exactly b bits")

        #Convert
        output=[[0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0]]
        for x in range(5):
            for y in range(5):
                offset=2*((5*y+x)*self.w)//8
                output[x][y]=self.fromHexStringToLane(string[offset:offset+(2*self.w//8)])
        return output

    def convertTableToStr(self, table):
        """
        Convert a 5×5 matrix representation to its string representation
        """

        #Check input format
        if self.w % 8 != 0:
            raise KeccakError.KeccakError("w is not a multiple of 8")
        if (len(table) !=  5) or (False in [len(row) == 5 for row in table]):
            raise KeccakError.KeccakError("Table must be 5×5")

        #Convert
        output= [''] * 25
        for x in range(5):
            for y in range(5):
                output[5*y+x] = self.fromLaneToHexString(table[x][y])
        output =''.join(output).upper()
        return output

    def absorb(self, P):
        for i in range((len(P)*8//2) // self.r):
            Pi=self.convertStrToTable(P[i*(2*self.r//8):(i+1)*(2*self.r//8)]+'00'*(self.c//8))

            for y in range(5):
              for x in range(5):
                  self.S[x][y] = self.S[x][y]^Pi[x][y]
            self.S = KeccakF.KeccakF(self.S, self.w, self.nr, self.verbose)

        if self.verbose:
            print("Value after absorption : %s" % (self.convertTableToStr(self.S)))

    def squeeze(self):
        Z = ''
        outputLength = self.n
        while outputLength > 0:
            string = self.convertTableToStr(self.S)
            Z = Z + string[:self.r*2//8]
            outputLength -= self.r
            if outputLength > 0:
                self.S = KeccakF.KeccakF(self.S, self.w, self.nr, self.verbose)

            # NB: done by block of length r, could have to be cut if outputLength
            #     is not a multiple of r

        if self.verbose:
            print("Value after squeezing : %s" % (self.convertTableToStr(self.S)))

        return Z[:2*self.n//8]

    def Keccak(self, M):
        """
        Compute the Keccak[r,c,d] sponge function on message M

        M: message pair (length in bits, string of hex characters ('9AFC...')
        """
        #Padding of messages
        P = self.pad10star1(M, self.r)

        if self.verbose:
            print("String ready to be absorbed: %s (will be completed by %d x '00')" % (P, c//8))

        self.absorb(P) 
        return self.squeeze()

