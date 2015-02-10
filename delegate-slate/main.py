#!/usr/bin/python
import bitsharesrpc
import sys
sys.path.append('..')
import config

if __name__ == "__main__":
 print( "Opening connection to client" )
 rpc = bitsharesrpc.client(config.url, config.user, config.passwd)

 print( "Opening wallet %s" % config.wallet )
 ret = rpc.wallet_open(config.wallet)

 print( "Unlocking wallet" )
 ret = rpc.unlock(999999, config.unlock)

 # get all accounts known to the client
 accounts = rpc.wallet_list_accounts()["result"]

 print( "Unapproving all previously approve delegates" )
 for account in accounts :
  rpc.wallet_approve_delegate(account["name"], "0")

 print( "Approving trusted delegates" )
 for d in config.trusted :
  print( " - %s" % d )
  rpc.wallet_approve_delegate(d)

 ## publish slate
 ret = rpc.wallet_publish_slate(config.slatedelegate, config.slatepayee)

 ## dump publish transaction as a whole
 print("Broadcasting slate")
 print("Transactions ID: %s" % ret["result"]["record_id"])

 ## close wallet
 rpc.lock()
