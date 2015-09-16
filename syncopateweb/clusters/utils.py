import sys
import re

def fnv32a( str ):
    hval = 0x811c9dc5
    fnv_32_prime = 0x01000193
    uint32_max = 2 ** 32
    for s in str:
        hval = hval ^ ord(s)
        hval = (hval * fnv_32_prime) % uint32_max
    return hval

def genToken( key ):
    salt = "AB#*FP"
    return fnv32a("%s%s" % (salt,key))