

class KeccakHash:

    def __init__(self, sponge):
        """
        Compute the Keccak[r,c,d] sponge function on message M

        """
        #Padding of messages
        P = self.pad10star1(M, self.r)

        if self.verbose:
            print("String ready to be absorbed: %s (will be completed by %d x '00')" % (P, c//8))

        self.absorb(P) 
        return self.squeeze()

    def hash(
        M: message pair (length in bits, string of hex characters ('9AFC...')
