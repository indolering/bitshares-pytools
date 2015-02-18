import json
import struct
import binascii
import hashlib
import math
import genbtskey as btskey
import ecdsa
import sys
from pprint import pprint
import time

def varint(n):
    if n < 0xfd:
        return struct.pack('<B', n)
    elif n < 0xffff:
        return struct.pack('<cH', '\xfd', n)
    elif n < 0xffffffff:
        return struct.pack('<cL', '\xfe', n)
    else:
        return struct.pack('<cQ', '\xff', n)

def variable_buffer( s ) :
    return varint(len(s)) + s

def derSigToHexSig(s):
    s, junk = ecdsa.der.remove_sequence(s.decode('hex'))
    if junk != '':
        print('JUNK', junk.encode('hex'))
    assert(junk == '')
    x, s = ecdsa.der.remove_integer(s)
    y, s = ecdsa.der.remove_integer(s)
    return '%064x%064x' % (x, y)

def recoverPubkeyParameter(digest, signature, pubkey) :
    for i in xrange(0,4) :
        p = signature_to_public_key(digest, signature, i)
        if p.to_string() == pubkey.to_string() :
            return i
    return None

def signature_to_public_key(digest, signature, i):
    # See http://www.secg.org/download/aid-780/sec1-v2.pdf section 4.1.6 primarily
    curve = ecdsa.SECP256k1.curve
    G     = ecdsa.SECP256k1.generator
    order = ecdsa.SECP256k1.order

    isYOdd      = i % 2
    isSecondKey = i // 2
    yp = 0 if (isYOdd) == 0 else 1

    r, s = ecdsa.util.sigdecode_string(signature, order)
    
    # 1.1
    x = r + isSecondKey * order

    # 1.3. This actually calculates for either effectively 02||X or 03||X depending on 'k' instead of always for 02||X as specified.
    # This substitutes for the lack of reversing R later on. -R actually is defined to be just flipping the y-coordinate in the elliptic curve.
    alpha = ((x * x * x) + (curve.a() * x) + curve.b()) % curve.p()
    beta = ecdsa.numbertheory.square_root_mod_prime(alpha, curve.p())
    if (beta - yp) % 2 == 0:
        y = beta
    else:
        y = curve.p() - beta

    # 1.4 Constructor of Point is supposed to check if nR is at infinity. 
    R = ecdsa.ellipticcurve.Point(curve, x, y, order)
    
    # 1.5 Compute e
    e = ecdsa.util.string_to_number(digest)

    # 1.6 Compute Q = r^-1(sR - eG)
    Q = ecdsa.numbertheory.inverse_mod(r, order) * (s * R + (-e % order) * G)

    # Not strictly necessary, but let's verify the message for paranoia's sake.
    #if ecdsa.VerifyingKey.from_public_point(Q, curve=ecdsa.SECP256k1).verify_digest(signature, digest, sigdecode=ecdsa.util.sigdecode_string) != True:
    #    return None
    #return Q
    return ecdsa.VerifyingKey.from_public_point(Q, curve=ecdsa.SECP256k1)



'''

delegate (unlocked) >>> blockchain_list_address_balances BTS5YRcZ2mdG1MjSYV4jBoZsX9zqf9FcfkHm                                                                                                        
[[
    "BTSHbogUDzjTXtz9449LgyyXBTCGY7s1i8ZR",{
      "condition": {
        "asset_id": 22,
        "slate_id": 0,
        "type": "withdraw_signature_type",
        "data": {
          "owner": "BTS5YRcZ2mdG1MjSYV4jBoZsX9zqf9FcfkHm",
          "memo": null
        }
      },
      "balance": 10000,
      "restricted_owner": null,
      "snapshot_info": null,
      "deposit_date": "2015-02-15T10:00:00",
      "last_update": "2015-02-15T10:00:00",
      "meta_data": null
    }
  ],[
    "BTSHg6u25QeafziQUrGg6Z3uNAh1S8ML4jq3",{
      "condition": {
        "asset_id": 0,
        "slate_id": 927401178929949429,
        "type": "withdraw_signature_type",
        "data": {
          "owner": "BTS5YRcZ2mdG1MjSYV4jBoZsX9zqf9FcfkHm",
          "memo": null
        }
      },
      "balance": 100000,
      "restricted_owner": null,
      "snapshot_info": null,
      "deposit_date": "2015-02-15T10:08:10",
      "last_update": "2015-02-15T10:08:10",
      "meta_data": null
    }
  ]
]

'''

chainid        = "75c11a81b7670bbaa721cc603eadb2313756f94a3bcbb9928e9101432701ac5f"
PREFIX         = "BTS"
receiveAddress = "BTSEhd3j4R4rdKGpLHX5SgEUN1p3zs4A58q1"
balance_id     = "BTSHg6u25QeafziQUrGg6Z3uNAh1S8ML4jq3"
privKey        = btskey.wifKeyToPrivateKey("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX").decode('hex')
otk            = None
asset_id       = 0   # BTS
slate_id       = 0   # no slate
fee            = .1 * 1e5
amount         = 1*1e5 - fee

owner                  = btskey.btsbase58CheckDecode(receiveAddress[len(PREFIX):])
balanceid              = btskey.btsbase58CheckDecode(balance_id[len(PREFIX):])
memo_data              = ""
withdraw_cond_type     = 1  # withdraw_signature_type
claim_input_data       = ""

### WithdrawSignatureType
withdraw_data  = struct.pack("<20s",owner)
if otk : 
    memo_otk       = btskey.btsbase58CheckDecode(otk[len(PREFIX):])
    withdraw_data += struct.pack("<B", 0x01)   ## optional True/False
    withdraw_data += struct.pack("<33s",memo_otk)
    withdraw_data += variable_buffer( memo_data )
else :
    withdraw_data += struct.pack("<B", 0x00)   ## optional True/False
print("="*10+"WithdrawData")
print (binascii.hexlify(withdraw_data))

### WithdrawCondition
withdraw_condition  = varint(asset_id)
withdraw_condition += struct.pack("<Q",slate_id) 
withdraw_condition += struct.pack("<B",withdraw_cond_type) 
withdraw_condition += variable_buffer(withdraw_data)
print("="*10+"WithdrawCondition")
print (binascii.hexlify(withdraw_condition))

### Deposit
deposit  = struct.pack("<Q",amount)
deposit += withdraw_condition
print("="*10+"Deposit")
print(binascii.hexlify(deposit))

### Withdraw
withdraw  = struct.pack("<20s",balanceid)
withdraw += struct.pack("<Q",amount+fee)
withdraw += variable_buffer(claim_input_data)
print("="*10+"Withdraw")
print(binascii.hexlify(withdraw))

### Operations
depositOp  = struct.pack("<B",0x2)  # deposit_op_type = 2;
depositOp += variable_buffer(deposit)
print(binascii.hexlify(depositOp))

withdrawOp  = struct.pack("<B",0x1) # withdraw_op_type = 1;
withdrawOp += variable_buffer(withdraw)
print(binascii.hexlify(withdrawOp))

operations = depositOp + withdrawOp
numOperations = 2

### Transaction
expiration   = time.time() + ( 60*60*24 )
#expiration   = math.floor(expiration/1000)
print(expiration)
transaction  = struct.pack("<I",expiration)  ## expiration time
transaction += struct.pack("<B",0x0)         ## true/false slate_id
transaction += varint(numOperations)
transaction += operations
print("="*10+"Transaction")
print(binascii.hexlify(transaction))

### Message to Sign
sigMessage   = transaction
sigMessage  += binascii.unhexlify(chainid)

## Signing Process
sk        = ecdsa.SigningKey.from_string(privKey, curve=ecdsa.SECP256k1)
sigder    = sk.sign_deterministic(sigMessage, hashfunc=hashlib.sha256,sigencode=ecdsa.util.sigencode_der)
hexSig    = derSigToHexSig(binascii.hexlify(sigder))  # DER decode
signature = binascii.unhexlify(hexSig)
r, s      = ecdsa.util.sigdecode_string(signature, ecdsa.SECP256k1.order)
assert sk.get_verifying_key().verify(signature, sigMessage, hashfunc=hashlib.sha256) ## verify valid pubkey
assert ecdsa.curves.orderlen( r ) == 32 ## Verify length or r and s
assert ecdsa.curves.orderlen( s ) == 32 ## Verify length or r and s
i = recoverPubkeyParameter(hashlib.sha256(sigMessage).digest(), signature, sk.get_verifying_key())
i += 4 #compressed
i += 27 #compact

signedTransaction = transaction
signedTransaction += varint( 1 )           # number of signatures
signedTransaction += struct.pack("<B",i)   # recovery parameter
signedTransaction += signature             # signature

print("="*10+"Signed Transaction")
print(binascii.hexlify(signedTransaction))
