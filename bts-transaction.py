#!/usr/bin/env python2

import ecdsa
import hashlib
import os
import sys
import unittest
import struct
from binascii import hexlify
from genbtskey import *

enc_memo_hex = "" # enc with otk_private
tx1_balance_id = "BTS5bJNzfPVQxEahXp28H85hnL9GvdbiHdPf"

def trx( privkey, topubkey, amount, asset_id, balance_id ) :
    fee               = .5 * 1e5

    #####################
    # Withdraw condition for deposit ( equals 'output' )
    #owner                  = ripemd160(hashlib.sha512(topubkey).digest())
    owner                  = btsbase58CheckDecode("XTS8QZgeFurRa6hzZVDtUDfvg7u7LAySeuNK")
    memo_otk               = btsbase58CheckDecode("XTS54pK2P15bth1C4v9QLtMQDuV7vR8RQQttMBHMzScrJdG7GsBza")
    memo_data              = ""
    slate_id               = 0
    type_id                = 1 # withdraw_signature_type
    values                 = ( owner, memo_otk, memo_data )
    withdraw_sig_condition = struct.pack('<20sss',*values)
    print ("withdraw_sig_condition: "+hexlify(withdraw_sig_condition))
    values                 = ( asset_id, slate_id, type_id )
    wc                     = struct.pack("<iqb",*values) + withdraw_sig_condition
    print ("withdraw_condition: " + hexlify(wc))


    print("soll: 1600000000000000000137513dbafc2b1e175d91e3d7d71181b9742fdf90dc01021772ca67d26ed39f30580bb7e2ac5952bba74de08db7246b19c7ad0ae439280e00")
#     deposit                = struct.pack("<q", amount) + wc # Deposit operation ( this will be the complete 'output' )
#     print ("deposit: " + hexlify(deposit))
# 
#     #####################
#     # Withdraw
#     balanceAddressRaw = base58decode(balance_id[ len( PREFIX ): ])
#     balanceAddress    = balanceAddressRaw[ :20 ] ## fixme check checksum
#     claim_input_data  = ""
#     values            = ( balanceAddress, amount+fee, len(claim_input_data), claim_input_data)
#     withdraw          = struct.pack('<20sids',*values)
#     print (hexlify(withdraw))

if __name__ == '__main__':
    private_key = os.urandom(32).encode('hex')

    # Output
    print "Secret Exponent         : %s " % private_key 
    print "Private Key             : %s " % privateKeyToWif(private_key)
    print "-"*80
    print "BTS PubKey              : %s " % keyToBTSPubKey(private_key)
    print "BTS Address             : %s " % keyToBTSAddress(private_key)
    print "-"*80

    print trx( private_key, "", 10*1e5, 0, tx1_balance_id )


# wc = bts.blockchain.WithdrawCondition.fromJson({                                                                                                                                                                                          
# "asset_id": 22,                                                                                                                                                                                       
# "slate_id": 0,                                                                                                                                                                                        
# "type": "withdraw_signature_type",                                                                                                                                                                    
# "data": {                                                                                                                                                                                             
# "owner": "XTS8QZgeFurRa6hzZVDtUDfvg7u7LAySeuNK",                                                                                                                                                    
# "memo": {                                                                                                                                                                                           
# "one_time_key": "XTS54pK2P15bth1C4v9QLtMQDuV7vR8RQQttMBHMzScrJdG7GsBza",                                                                                                                          
# "encrypted_memo_data": ""                                         
# } } })
# Object { asset_id: 22, slate_id: 0, type_id: 1, condition: Object }
# wc.toHex()
# "1600000000000000000137513dbafc2b1e175d91e3d7d71181b9742fdf90dc01021772ca67d26ed39f30580bb7e2ac5952bba74de08db7246b19c7ad0ae439280e00"
# 
# wc.condition
# Object { owner: Uint8Array[20], one_time_key: Object, encrypted_memo: Uint8Array[0], type_name: "withdraw_signature_type", type_id: undefined }
# 
# # 
