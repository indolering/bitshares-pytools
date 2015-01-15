#!/usr/bin/env python2

import ecdsa
import hashlib
import os
import sys
import unittest
import struct
from binascii import hexlify

enc_memo_hex = "" # enc with otk_private
tx1_balance_id = "BTS5bJNzfPVQxEahXp28H85hnL9GvdbiHdPf"

# https://github.com/gferrin/bitcoin-code/blob/master/utils.py
b58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

PREFIX = "BTS"

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
    
def compressedpubkey(s):
    # https://github.com/lyndsysimon/cryptocoin/blob/master/cryptocoin/key.py 
    point = ecdsa.SigningKey.from_string(s.decode('hex'), curve=ecdsa.SECP256k1).verifying_key.pubkey.point
    x = hex(point.x())[2:].strip('L')
    y = hex(point.y())[2:].strip('L')
    return ''.join(( '02' if point.y() % 2 == 0 else '03', x))

def keyToPubKey(s): # raw pubkey
    btspubkey  = compressedpubkey(s).decode('hex')
    return base58encode(base256decode(btspubkey))

def keyToBTSPubKey(s):
    btspubkey  = compressedpubkey(s).decode('hex')
    myhash     = ripemd160(btspubkey)
    return PREFIX + base58encode(base256decode(btspubkey + myhash[ :4 ]))

def keyToBTSAddress(s) :
    btspubkey  = compressedpubkey(s).decode('hex')
    myaddress  = ripemd160(hashlib.sha512(btspubkey).digest())
    myhash     = ripemd160(myaddress)
    return PREFIX + base58encode(base256decode(myaddress + myhash[ :4 ]))

def pubkeyToBTSAddress(s) :
    btspubkey  = s.decode('hex')
    myaddress  = ripemd160(hashlib.sha512(btspubkey).digest())
    myhash     = ripemd160(myaddress)
    return PREFIX + base58encode(base256decode(myaddress + myhash[ :4 ]))

def trx( privkey, topubkey, amount, asset_id, balance_id ) :
    fee               = .5 * 1e5

    #####################
    # Withdraw condition for deposit ( equals 'output' )
    owner                  = ripemd160(hashlib.sha512(topubkey).digest())
    memo_otk               = ""
    memo_data              = ""
    slate_id               = 0
    type_id                = 1 # withdraw_signature_type
    values                 = ( owner, memo_otk, memo_data )
    withdraw_sig_condition = struct.pack('<20sss',*values)
    print ("withdraw_sig_condition: "+hexlify(withdraw_sig_condition))
    values                 = ( asset_id, slate_id, type_id )
    wc                     = struct.pack("<iqb",*values) + withdraw_sig_condition
    print ("withdraw_condition: " + hexlify(wc))
    deposit                = struct.pack("<q", amount) + wc # Deposit operation ( this will be the complete 'output' )
    print ("deposit: " + hexlify(deposit))

    #####################
    # Withdraw
    balanceAddressRaw = base256encode(base58decode(balance_id[ len( PREFIX ): ]))
    balanceAddress    = balanceAddressRaw[ :20 ] ## fixme check checksum
    claim_input_data  = ""
    values            = ( balanceAddress, amount+fee, len(claim_input_data), claim_input_data)
    withdraw          = struct.pack('<20sids',*values)
    print (hexlify(withdraw))

if __name__ == '__main__':
    private_key = os.urandom(32).encode('hex')

    # Output
    print "Secret Exponent         : %s " % private_key 
    print "Private Key             : %s " % privateKeyToWif(private_key)
    print "-"*80
    print "BTS PubKey              : %s " % keyToBTSPubKey(private_key)
    print "BTS Address             : %s " % keyToBTSAddress(private_key)
    print "-"*80

    print trx( private_key, keyToPubKey(private_key), 10*1e5, 0, tx1_balance_id )


wc = bts.blockchain.WithdrawCondition.fromJson({                                                                                                                                                                                          
"asset_id": 22,                                                                                                                                                                                       
"slate_id": 0,                                                                                                                                                                                        
"type": "withdraw_signature_type",                                                                                                                                                                    
"data": {                                                                                                                                                                                             
"owner": "XTS8QZgeFurRa6hzZVDtUDfvg7u7LAySeuNK",                                                                                                                                                    
"memo": {                                                                                                                                                                                           
"one_time_key": "XTS54pK2P15bth1C4v9QLtMQDuV7vR8RQQttMBHMzScrJdG7GsBza",                                                                                                                          
"encrypted_memo_data": ""                                         
} } })
Object { asset_id: 22, slate_id: 0, type_id: 1, condition: Object }
wc
Object { asset_id: 22, slate_id: 0, type_id: 1, condition: Object }
wc.toHex()
"1600000000000000000177513dbafc2b1e175d91e3d7d71181b9742fdf90dc01021772ca67d26ed39f30580bb7e2ac5952bba74de08db7246b19c7ad0ae439280e404a2c983ebe4b5ee84cdf21f27c730d1aaf577e24e5a3649a1404cc521ed8644a760f53eb6936ffe68a7fea26a5a7970f71d4700d2eb8452c0dfe514f26948e21"
wc.condition
Object { owner: Uint8Array[20], one_time_key: Object, encrypted_memo: Uint8Array[0], type_name: "withdraw_signature_type", type_id: undefined }



wc = bts.blockchain.WithdrawCondition.fromJson({                                                                                                                                                                                          
"asset_id": 22,                                                                                                                                                                                       
"slate_id": 0,                                                                                                                                                                                        
"type": "withdraw_signature_type",                                                                                                                                                                    
"data": {                                                                                                                                                                                             
"owner": "XTS8QZgeFurRa6hzZVDtUDfvg7u7LAySeuNK",                                                                                                                                                    
"memo": {                                                                                                                                                                                           
"one_time_key": "XTS54pK2P15bth1C4v9QLtMQDuV7vR8RQQttMBHMzScrJdG7GsBza",                                                                                                                          
"encrypted_memo_data": ""                                         
} } })
Object { asset_id: 22, slate_id: 0, type_id: 1, condition: Object }
wc.toHex()
"1600000000000000000137513dbafc2b1e175d91e3d7d71181b9742fdf90dc01021772ca67d26ed39f30580bb7e2ac5952bba74de08db7246b19c7ad0ae439280e00"

wc.condition
Object { owner: Uint8Array[20], one_time_key: Object, encrypted_memo: Uint8Array[0], type_name: "withdraw_signature_type", type_id: undefined }


