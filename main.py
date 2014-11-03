#!/usr/bin/python
from btsrpcapi import *
import config

if __name__ == "__main__":
 ## open up connection to client
 print( "Opening connection to client" )
 rpc = btsrpcapi(config.url, config.user, config.passwd)

 ## open wallet
 print( "Opening wallet %s" % config.wallet )
 ret = rpc.walletopen(config.wallet)
 if ret == -1 : raise Exception( "Failed to open wallet! Connection settings ok?" )

 ## unlock wallet
 print( "Unlocking wallet" )
 ret = rpc.unlock(config.unlock)
 if ret == -1 : raise Exception( "Failed to unlock wallet! Wallet and connection settings ok?" )
 if "error" in ret : raise Exception( "Error unlock wallet! Check passphrase" )

 # get all accounts known to the client
 accounts = rpc.walletallgetaccounts()["result"]

 ## unapprove ALL accounts
 print( "Unapproving all previously approve delegates" )
 for account in accounts :
  rpc.unapprovedelegate(account["name"])

 ## approve trusted accounts
 print( "Approving trusted delegates" )
 for d in config.trusted :
  print( " - %s" % d )
  rpc.approvedelegate(d)

 ## publish slate
 ret = rpc.publishslate(config.delegate, config.payee)
 if ret == -1 : raise Exception( "Failed to unlock wallet! Wallet and connection settings ok?" )
 if "error" in ret : raise Exception( "Unable to publish slate?! WTF? Got:\n %s" % ret )

 ## dump publish transaction as a whole
 print("Broadcasting slate")
 print("Transactions ID: %s" % ret["result"]["record_id"])
 #print(json.dumps(ret,indent=4))
