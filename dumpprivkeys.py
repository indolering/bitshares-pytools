#!/usr/bin/python

from btsrpcapi import *
import config
  
if __name__ == "__main__":
 rpc = btsrpcapi(config.url, config.user, config.passwd)
 print rpc.info()
 print rpc.wallet_open(config.wallet)
 rpc.unlock(9999,config.unlock)
 r = (rpc.wallet_list_my_accounts())
 accounts = r["result"]
 print "---------------------------------------------------------------------------------"
 for account in accounts :
  print "%20s - %s - %s" % (account["name"], account["owner_key"], rpc.wallet_dump_private_key(account["owner_key"]))
 print "---------------------------------------------------------------------------------"
 print rpc.lock()
