# -*- coding: utf-8 -*-

class KeccakUtil:

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
  r=[[0,    36,     3,    41,    18]    ,
     [1,    44,    10,    45,     2]    ,
     [62,    6,    43,    15,    61]    ,
     [28,   55,    25,    21,    56]    ,
     [27,   20,    39,     8,    14]    ]

  def __init__(self, b):
    self.b = b
    self.w = b // 25

  ## Generic utility functions
  def rot(self,x,n):
      """Bitwise rotation (to the left) of n bits considering the \
      string of bits is w bits long"""

      n = n % self.w
      return ((x>>(self.w-n))+(x<<n))%(1<<self.w)

  def fromHexStringToLane(self, string):
      """Convert a string of bytes written in hexadecimal to a lane value"""

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
      """Convert a lane value to a string of bytes written in hexadecimal"""

      laneHexBE = (("%%0%dX" % (self.w//4)) % lane)
      #Perform the modification
      temp=''
      nrBytes=len(laneHexBE)//2
      for i in range(nrBytes):
          offset=(nrBytes-i-1)*2
          temp+=laneHexBE[offset:offset+2]
      return temp.upper()

  def printState(self, state, info):
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

  ### Conversion functions String <-> Table (and vice-versa)

  def convertStrToTable(self,string):
      """Convert a string of bytes to its 5×5 matrix representation

      string: string of bytes of hex-coded bytes (e.g. '9A2C...')"""

      #Check that input paramaters
      if self.w%8!= 0:
          raise KeccakError("w is not a multiple of 8")
      if len(string)!=2*(self.b)//8:
          raise KeccakError.KeccakError("string can't be divided in 25 blocks of w bits\
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

  def convertTableToStr(self,table):
      """Convert a 5×5 matrix representation to its string representation"""

      #Check input format
      if self.w % 8!= 0:
          raise KeccakError.KeccakError("w is not a multiple of 8")
      if (len(table)!=5) or (False in [len(row)==5 for row in table]):
          raise KeccakError.KeccakError("table must be 5×5")

      #Convert
      output=['']*25
      for x in range(5):
          for y in range(5):
              output[5*y+x]=self.fromLaneToHexString(table[x][y])
      output =''.join(output).upper()
      return output


