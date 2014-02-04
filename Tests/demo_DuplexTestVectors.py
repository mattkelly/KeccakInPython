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
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../Constructions')
import KeccakDuplex

dirTestVector = os.path.dirname(os.path.realpath(__file__))
verbose=False

#DuplexKAT_r1026c574.txt
#DuplexKAT_r1027c573.tx

#String comparison function (useful later to compare test vector and computation)
def sameString(string1, string2):
    """Compare 2 strings"""

    if len(string1)!=len(string2):
        return False
    for i in range(len(string1)):
        if string1[i]!=string2[i]:
            return False
    return True

#Open the corresponding file
try:
    #reference=open(os.path.join(dirTestVector, 'DuplexKAT_r1026c574.txt', 'r'))
    reference=open('DuplexKAT_r1026c574.txt', 'r')
except IOError:
    print("Error: test vector files must be stored in %s" % (dirTestVector))
    exit()

#Parse the document line by line (works only for Short and Long files)
for line in reference:
    if line.startswith('InLen'):
        inLen=int(line.split(' = ')[1].strip('\n\r'))
    if line.startswith('In'):
        inData=line.split(' = ')[1].strip('\n\r')
    if line.startswith('OutLen'):
        outLen=int(line.split(' = ')[1].strip('\n\r'))
    if line.startswith('Out'):
        outData=line.split(' = ')[1].strip('\n\r')

        #if line.startswith('Squeezed'):
            #n = (len(MD_ref)//2)*8
        #elif n == 0:
            #print("Error: the output length should be specified")
            #exit()

        # Perform our own computation
        #MD_comp=myKeccak.Keccak((Len,Msg), r, c, n, verbose)
        myDuplex = KeccakDuplex.KeccakDuplex(1026, 574, verbose)
        MD_comp = myKeccak.Keccak((inLen,inData), 1026)

        #Compare the results
        if not sameString(MD_comp, outData):
            print('ERROR: \n\t type=%s\n\t length=%d\n\t message=%s\n\t reference=%s\n\t computed=%s' % (suffix, inLen, inData, outData, MD_comp))
            exit()

print("OK\n")
reference.close()
