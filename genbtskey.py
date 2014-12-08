#!/usr/bin/env python2

import ecdsa
import hashlib
import os
import sys
import unittest

# https://github.com/gferrin/bitcoin-code/blob/master/utils.py
b58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58encode(n):
    result = ''
    while n > 0:
        result = b58[n%58] + result
        n /= 58
    return result

def base58decode(s):
    result = 0
    for i in range(0, len(s)):
        result = result * 58 + b58.index(s[i])
    return result

def base256decode(s):
    result = 0
    for c in s:
        result = result * 256 + ord(c)
    return result

def base256encode(n):
    result = ''
    while n > 0:
        result = chr(n % 256) + result
        n /= 256
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

def base58CheckDecode(s):
    leadingOnes = countLeadingChars(s, '1')
    s = base256encode(base58decode(s))
    result = '\0' * leadingOnes + s[:-4]
    chk = s[-4:]
    checksum = hashlib.sha256(hashlib.sha256(result).digest()).digest()[0:4]
    assert(chk == checksum)
    version = result[0]
    return result[1:]

def wifKeyToPrivateKey(s) :
        return base58CheckDecode(s).encode('hex')

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

class Testcases(unittest.TestCase) :
    def test_btspubkey(self):
        self.assertEqual(keyToBTSPubKey(wifKeyToPrivateKey("5HqUkGuo62BfcJU5vNhTXKJRXuUi9QSE6jp8C3uBJ2BVHtB8WSd")),"BTS677ZZd62Ca7SoUJoT1CytBhj4aJewzzi8tQZxYNqpSSK69FTuF")
        self.assertEqual(keyToBTSPubKey(wifKeyToPrivateKey("5JWcdkhL3w4RkVPcZMdJsjos22yB5cSkPExerktvKnRNZR5gx1S")),"BTS5z5e3BawwMY6UmcBQxYpkKZ8QQm4wdtS4KMZiWAcWBUC3RJuLT")
        self.assertEqual(keyToBTSPubKey(wifKeyToPrivateKey("5HvVz6XMx84aC5KaaBbwYrRLvWE46cH6zVnv4827SBPLorg76oq")),"BTS7W5qsanXHgRAZPijbrLMDwX6VmHqUdL2s8PZiYKD5h1R7JaqRJ")
        self.assertEqual(keyToBTSPubKey(wifKeyToPrivateKey("5Jete5oFNjjk3aUMkKuxgAXsp7ZyhgJbYNiNjHLvq5xzXkiqw7R")),"BTS86qPFWptPfUNKVi6hemeEWshoLerN6JvzCvFjqnRSEJg7nackU")
        self.assertEqual(keyToBTSPubKey(wifKeyToPrivateKey("5KDT58ksNsVKjYShG4Ls5ZtredybSxzmKec8juj7CojZj6LPRF7")),"BTS57qhJwt9hZtBsGgV7J5ZPHFi5r5MEeommYnFpDb6grK3qev2qX")

    def test_btsaddress(self):
        self.assertEqual(keyToBTSAddress(wifKeyToPrivateKey("5HqUkGuo62BfcJU5vNhTXKJRXuUi9QSE6jp8C3uBJ2BVHtB8WSd")),"BTSFN9r6VYzBK8EKtMewfNbfiGCr56pHDBFi")
        self.assertEqual(keyToBTSAddress(wifKeyToPrivateKey("5JWcdkhL3w4RkVPcZMdJsjos22yB5cSkPExerktvKnRNZR5gx1S")),"BTSdXrrTXimLb6TEt3nHnePwFmBT6Cck112")
        self.assertEqual(keyToBTSAddress(wifKeyToPrivateKey("5HvVz6XMx84aC5KaaBbwYrRLvWE46cH6zVnv4827SBPLorg76oq")),"BTSJQUAt4gz4civ8gSs5srTK4r82F7HvpChk")
        self.assertEqual(keyToBTSAddress(wifKeyToPrivateKey("5Jete5oFNjjk3aUMkKuxgAXsp7ZyhgJbYNiNjHLvq5xzXkiqw7R")),"BTSFPXXHXXGbyTBwdKoJaAPXRnhFNtTRS4EL")
        self.assertEqual(keyToBTSAddress(wifKeyToPrivateKey("5KDT58ksNsVKjYShG4Ls5ZtredybSxzmKec8juj7CojZj6LPRF7")),"BTS3qXyZnjJneeAddgNDYNYXbF7ARZrRv5dr")

    def test_btcaddress(self):
        self.assertEqual(keyToBTCAddress(wifKeyToPrivateKey("5HqUkGuo62BfcJU5vNhTXKJRXuUi9QSE6jp8C3uBJ2BVHtB8WSd")),"141fYYgjgTfxWCzUhFwVrad54EWi8Yw29a")
        self.assertEqual(keyToBTCAddress(wifKeyToPrivateKey("5JWcdkhL3w4RkVPcZMdJsjos22yB5cSkPExerktvKnRNZR5gx1S")),"19854zGaBhcgHV2hZa6bzqMBW5kHCbw7YA")
        self.assertEqual(keyToBTCAddress(wifKeyToPrivateKey("5HvVz6XMx84aC5KaaBbwYrRLvWE46cH6zVnv4827SBPLorg76oq")),"1G7qw8FiVfHEFrSt3tDi6YgfAdrDrEM44Z")
        self.assertEqual(keyToBTCAddress(wifKeyToPrivateKey("5Jete5oFNjjk3aUMkKuxgAXsp7ZyhgJbYNiNjHLvq5xzXkiqw7R")),"12c7KAAZfpREaQZuvjC5EhpoN6si9vekqK")
        self.assertEqual(keyToBTCAddress(wifKeyToPrivateKey("5KDT58ksNsVKjYShG4Ls5ZtredybSxzmKec8juj7CojZj6LPRF7")),"1Gu5191CVHmaoU3Zz3prept87jjnpFDrXL")

    def test_wif(self):
        self.assertEqual(wifKeyToPrivateKey("5HqUkGuo62BfcJU5vNhTXKJRXuUi9QSE6jp8C3uBJ2BVHtB8WSd"),"02b52e04a0acfe611a4b6963462aca94b6ae02b24e321eda86507661901adb49")
        self.assertEqual(wifKeyToPrivateKey("5JWcdkhL3w4RkVPcZMdJsjos22yB5cSkPExerktvKnRNZR5gx1S"),"5b921f7051be5e13e177a0253229903c40493df410ae04f4a450c85568f19131")
        self.assertEqual(wifKeyToPrivateKey("5HvVz6XMx84aC5KaaBbwYrRLvWE46cH6zVnv4827SBPLorg76oq"),"0e1bfc9024d1f55a7855dc690e45b2e089d2d825a4671a3c3c7e4ea4e74ec00e")
        self.assertEqual(wifKeyToPrivateKey("5Jete5oFNjjk3aUMkKuxgAXsp7ZyhgJbYNiNjHLvq5xzXkiqw7R"),"6e5cc4653d46e690c709ed9e0570a2c75a286ad7c1bc69a648aae6855d919d3e")
        self.assertEqual(wifKeyToPrivateKey("5KDT58ksNsVKjYShG4Ls5ZtredybSxzmKec8juj7CojZj6LPRF7"),"b84abd64d66ee1dd614230ebbe9d9c6d66d78d93927c395196666762e9ad69d8")

    def test_fiw(self):
        self.assertEqual("5HqUkGuo62BfcJU5vNhTXKJRXuUi9QSE6jp8C3uBJ2BVHtB8WSd",privateKeyToWif("02b52e04a0acfe611a4b6963462aca94b6ae02b24e321eda86507661901adb49"))
        self.assertEqual("5JWcdkhL3w4RkVPcZMdJsjos22yB5cSkPExerktvKnRNZR5gx1S",privateKeyToWif("5b921f7051be5e13e177a0253229903c40493df410ae04f4a450c85568f19131"))
        self.assertEqual("5HvVz6XMx84aC5KaaBbwYrRLvWE46cH6zVnv4827SBPLorg76oq",privateKeyToWif("0e1bfc9024d1f55a7855dc690e45b2e089d2d825a4671a3c3c7e4ea4e74ec00e"))
        self.assertEqual("5Jete5oFNjjk3aUMkKuxgAXsp7ZyhgJbYNiNjHLvq5xzXkiqw7R",privateKeyToWif("6e5cc4653d46e690c709ed9e0570a2c75a286ad7c1bc69a648aae6855d919d3e"))
        self.assertEqual("5KDT58ksNsVKjYShG4Ls5ZtredybSxzmKec8juj7CojZj6LPRF7",privateKeyToWif("b84abd64d66ee1dd614230ebbe9d9c6d66d78d93927c395196666762e9ad69d8"))

if __name__ == '__main__':
    # unittest.main()
    # Generate a random private key or take it from input as WIF
    if len( sys.argv ) < 2 :
        private_key = os.urandom(32).encode('hex')
    else :
        if sys.argv[1]=="test" : 
            exit(0)
        else :
            private_key =  wifKeyToPrivateKey(sys.argv[1])

    # Output
    print "Secret Exponent : %s " % private_key 
    print "Private Key     : %s " % privateKeyToWif(private_key)
    print "Address         : %s " % keyToBTCAddress(private_key)
    print "BTS PubKey      : %s " % keyToBTSPubKey(private_key)
    print "BTS Address     : %s " % keyToBTSAddress(private_key)
