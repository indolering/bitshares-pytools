#!/usr/bin/env python2

import ecdsa
import ecdsa.der
import ecdsa.util
import hashlib
import os
import re
import struct

b58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58encode(n):
    result = ''
    while n > 0:
        result = b58[n%58] + result
        n /= 58
    return result

def base256decode(s):
    result = 0
    for c in s:
        result = result * 256 + ord(c)
    return result

def countLeadingChars(s, ch):
    count = 0
    for c in s:
        if c == ch:
            count += 1
        else:
            break
    return count

# https://en.bitcoin.it/wiki/Base58Check_encoding
def base58CheckEncode(version, payload):
    s = chr(version) + payload
    checksum = hashlib.sha256(hashlib.sha256(s).digest()).digest()[0:4]
    result = s + checksum
    leadingZeros = countLeadingChars(result, '\0')
    return '1' * leadingZeros + base58encode(base256decode(result))

def privateKeyToWif(key_hex):    
    return base58CheckEncode(0x80, key_hex.decode('hex'))
    
def privateKeyToPublicKey(s):
    sk = ecdsa.SigningKey.from_string(s.decode('hex'), curve=ecdsa.SECP256k1)
    return ('\04' + sk.verifying_key.to_string()).encode('hex')

def ripemd160(s):
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(s)
    return ripemd160.digest()
    
def pubKeyToAddr(s):
    return base58CheckEncode(0, ripemd160(hashlib.sha256(s.decode('hex')).digest()))

def keyToBTCAddress(s):
    return pubKeyToAddr(privateKeyToPublicKey(s))

def compressedpubkey(s):
    # https://github.com/lyndsysimon/cryptocoin/blob/master/cryptocoin/key.py 
    point = ecdsa.SigningKey.from_string(s.decode('hex'), curve=ecdsa.SECP256k1).verifying_key.pubkey.point
    x = hex(point.x())[2:].strip('L')
    y = hex(point.y())[2:].strip('L')
    return ''.join(( '02' if point.y() % 2 == 0 else '03', x))

def keyToBTSPubKey(s):
    btspubkey  = compressedpubkey(s).decode('hex')
    myhash     = ripemd160(btspubkey)
    return "BTS" + base58encode(base256decode(btspubkey + myhash[ :4 ]))

def keyToBTSAddress(s) :
    btspubkey  = compressedpubkey(s).decode('hex')
    myaddress  = ripemd160(hashlib.sha512(btspubkey).digest())
    myhash     = ripemd160(myaddress)
    return "BTS" + base58encode(base256decode(myaddress + myhash[ :4 ]))

# Generate a random private key
private_key = os.urandom(32).encode('hex')

# Output
print "Secret Exponent : %s " % private_key 
print "Private Key     : %s " % privateKeyToWif(private_key)
print "Address         : %s " % keyToBTCAddress(private_key)
print "BTS PubKey      : %s " % keyToBTSPubKey(private_key)
print "BTS Address     : %s " % keyToBTSAddress(private_key)
