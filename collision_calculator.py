import sys
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Example datagram for encryption with AES-256. Datagram given as a list here, 
example_header = os.urandom(16)
example_payload = os.urandom(16)
example_datagram = [example_header,example_payload]
'print(example_datagram)'

def bad_hash(datagram):

    key = datagram[0]
    payload = datagram[1]
    iv = bytearray(16)

    # import the AES cipher with the header as the key. Use CBC mode with a 0 verctor for IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    aes = cipher.encryptor()
    cipher_text = aes.update(payload)

    # encrypt payload and xor header to output
    ct = int.from_bytes(cipher_text, byteorder=sys.byteorder)
    k = int.from_bytes(key, byteorder=sys.byteorder)
    return (ct ^ k).to_bytes(16, byteorder=sys.byteorder)

"print(bad_hash(example_datagram))"

# given a datagrm, we pick a random header (header_2) and use the digest from the first datagram to produce a payload_2
# such that the digest of datagram_2 = [header_2, payload_2] collides with the digest of the first datagram

def collision_finder(datagram):

    # to clarify notation use "_1" to signify the original datagram
    header_1 = datagram[0]

    # pick new random header
    header_2  = os.urandom(16)
    digest = bad_hash(datagram)
    iv = bytearray(16)

    # we require the key from the first hashing
    key_1 = datagram[0]
    
    # import the AES cipher again with a different key - the random header
    cipher_2 = Cipher(algorithms.AES(header_2), modes.CBC(iv))
    aes_inv_2 = cipher_2.decryptor()

    # construct the image of payload_2 under AES with header_2 as key, then find the inverse

    dig = int.from_bytes(digest, byteorder=sys.byteorder)
    hd2 = int.from_bytes(header_2, byteorder=sys.byteorder)
    payload_img = (dig ^ hd2).to_bytes(16, byteorder=sys.byteorder)
    payload_2 = aes_inv_2.update(payload_img)

    return [header_2, payload_2]

"print(collision_finder(example_datagram))"

def collision_checker(datagram_1,datagram_2):
    if bad_hash(datagram_1) == bad_hash(datagram_2):
        print(bad_hash(datagram_1), 'TRUE')
    else:
        print('Something went wrong...')


example_datagram_collision = collision_finder(example_datagram)

collision_checker(example_datagram, example_datagram_collision)