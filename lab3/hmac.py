import sys
from bitstring import BitArray
from sha256 import sha256



class hmac:

    def __init__(self):
        # Object for calculating SHA256 hashes
        self.hasher = sha256()

        # Create ipad and opad strings
        self.ipad = BitArray()
        self.opad = BitArray()

        while (self.ipad.length < 512):
            self.ipad.append('0x36')
        while (self.opad.length < 512):
            self.opad.append('0x5c')

    # Function to create an HMAC
    def create(self, messageBits, keyBits):

        # If the key is longer than the hash block size (512 bits for SHA256), the
        # key should be hashed. This should never get used by this program, which always takes in
        # a 256 bit SHA256 hash as a key, but it's part of the standard.
        if (keyBits.length > 512):
            keyBits = self.hasher.hash(keyBits)

        # Append bytes to the key until it is 512 bits long
        while (keyBits.length < 512):
            keyBits.append('0x00')

        # The first XOR operation is an XOR of the appended key and the ipad
        firstxor = keyBits ^ self.ipad

        # Hash the result of the first XOR operation with the message concatenated on
        firstHash = self.hasher.hash(firstxor + messageBits)

        # The second XOR operation is an XOR of the appended key and the opad
        secondxor = keyBits ^ self.opad

        # The mac is a hash of the second XOR concatenated with the first hash
        return self.hasher.hash(secondxor + firstHash)


if __name__ == '__main__':

    # Command line arguments for calling the hmac module
    keyFile = sys.argv[0]
    messageFile = sys.argv[1]
    outputFile = sys.argv[2]

    # Read in the message from the message file
    reader = open(messageFile, 'r')
    messageString = reader.read()
    reader.close()
    messageBits = BitArray(bytes=messageString.encode('utf8'))

    # Read in the key from the key file
    keyReader = open(keyFile, 'r')
    keyString = keyReader.read()
    keyBits = BitArray(hex=keyString)
    keyReader.close()



    # Call the hmac class's create function with the message and the key
    hmacGenerator = hmac()
    hmacResult = hmacGenerator.create(messageBits, keyBits)

    # Write the result to the output file
    writer = open(outputFile, 'w')
    writer.write(hmacResult.hex)
    writer.close()

