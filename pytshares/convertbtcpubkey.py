#!/usr/bin/env python2

import ecdsa
import hashlib
import os
import sys
import unittest
import genbtskey

if __name__ == '__main__':
    # unittest.main()
    # Generate a random private key or take it from input as WIF
    if len( sys.argv ) < 2 :
        raise( Exception( "Public Key required as argument" ) )
    else :
        pub_key =  (sys.argv[1])

    # Output
    if not pub_key[:2] == "02" and not pub_key[:2] == "03" :
        raise( Exception( "compressed key required" ) )
    print "BTC PubKey      : %s " % pub_key
    print "BTC Address     : %s " % genbtskey.pubKeyToAddr(pub_key)
    print "BTS PubKey      : %s " % genbtskey.btcPubkeytoBTSpubkey(pub_key)
    print "BTS Address     : %s " % genbtskey.btcPubKeyToBTSAddress(pub_key)
