#!/usr/bin/python
import bitsharesrpc
import config
import genbtskey
import os
from pprint import pprint

txfee = 0.5*1e5

if __name__ == "__main__":
 rpc = bitsharesrpc.client(config.url, config.user, config.passwd)
 rpc.wallet_open(config.wallet)
 rpc.unlock(999999, config.unlock)
 
 print("# Reading delegates")
 privkeys = []
 accounts = rpc.wallet_list_my_accounts()["result"]
 for account in accounts :
  if account["delegate_info"] :
   if not rpc.wallet_dump_private_key(account["owner_key"])["result"] :
    print("- %s (owner key not available! Skipping...)" % account["name"])
    continue
   if account["name"] == "delegate.xeroc" :
    print("- %s (paying account! Skipping...)" % account["name"])
    continue
   if rpc.market.get_balance( account["name"], 0 ) < txfee :
    print("- %s (Not funded! Requires %.2f BTS! Skipping...)" % (account["name"], txfee/1.0e5))
    continue
   print("- %s" % account["name"])
   ## store private keys in a variable
   p          = os.urandom(32).encode('hex')
   newprivkey = genbtskey.privateKeyToWif(p)
   newpubkey  = genbtskey.keyToBTSPubKey(p)
   privkeys.append({
                      "name" : account["name"],
                      "owner" : account["owner_key"],
                      "key" :rpc.wallet_dump_private_key(account["owner_key"])["result"],
                      "signingkey" : [newprivkey, newpubkey]
                   })
 print("# Import the new keys into your client's wallet")
 for d in privkeys : 
  print("- %s" % d["name"])
  try : 
   rpc.wallet_import_private_key(d["signingkey"][0], d["name"], False, False)
  except :
   print("error importing key")
   print("stopping!")
   raise # do not continue
 print("# Broadcasting change signing key transaction")
 for d in privkeys : 
  print("- %s" % d["name"])
  try :
   rpc.wallet_delegate_update_signing_key(d["name"], d["name"], d["signingkey"][1])
  except :
   print("Error changing signing key for %s. Probably not able to pay. Please fund account." % d["name"])
 print("# Import the new keys into your client manually!")
 for d in privkeys : 
  print("wallet_import_private_key %s" % d["signingkey"][0])
 print("# Important notice!!")
 print("Wait at LEAST 35 minutes before switching to the new\n"+\
       "wallet. The old and new signing keys have to be available for at least\n"+\
       "one block!")
