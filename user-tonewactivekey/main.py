#!/usr/bin/python
import bitsharesrpc
import config
import genbtskey
import os
from pprint import pprint

txfee = 0.1

rpc = bitsharesrpc.client(config.url, config.user, config.passwd)
rpc.wallet_open(config.wallet)
rpc.unlock(999999, config.unlock)

print("# Reading accounts")
accounts = rpc.wallet_list_my_accounts()["result"]

#########################################
#print("\n\n## setting new active keys")
#for account in accounts :
# print("- %20s" % account["name"])
# try :
#  rpc.wallet_account_update_active_key(account["name"], config.payee)
# except :
#  print("Error changing active key for %s. Probably not able to pay. Please fund account." % account["name"])
#  continue
#
#########################################
#print("\n\n## waiting two blocks to confirm")
#rpc.wait_for_block()
#rpc.wait_for_block()
#
########################################
print("\n\n## moving funds to new active keys")
for account in accounts :
 funds = rpc.balance(account["name"])["result"]
 if not funds or funds == [] or funds == None : continue
 for f in funds[0][1] : 
  if f[0] == 0 : continue
  asset  = rpc.blockchain_get_asset(f[0])["result"]
  symbol = asset["symbol"]
  precision = asset["precision"]
  amount = float(f[1])/precision
  if amount == 0.0: continue
  print("-- %20s : sending %f %s" % (account["name"], amount, symbol))
  rpc.wallet_transfer(amount, symbol, account["name"], account["name"], "new active key")

########################################
print("\n\n## waiting two blocks to confirm")
rpc.wait_for_block()
rpc.wait_for_block()

########################################
print("\n\n## moving remaining BTS to new active keys")
## Move BTS separatly as tx fees are payed from BTS
for account in accounts :
 amount    = rpc.market.get_balance(account["name"], "0") - txfee
 if amount > 0.0 :
  print("-- %20s : sending %f %s" % (account["name"], amount, symbol))
  rpc.wallet_transfer(amount, "BTS", account["name"], account["name"], "new active key")

########################################
print("\n\n## new active keys")
for account in accounts :
 privkey = rpc.wallet_dump_account_private_key(account["name"],"active_key")["result"]
 print("wallet_import_private_key %s false false" % privkey)

########################################
rpc.lock()
print("Wallet locked. Please issue a rescan if you don't see your funds!")
