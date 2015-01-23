#!/usr/bin/python
from btsrpcapi import *
import config
import re

payouttarget = "payouts.charity"
withdrawfee = 0.5 * 1e5;
rpc = btsrpcapi(config.url, config.user, config.passwd)

if __name__ == "__main__":
 print rpc.info()
 print rpc.wallet_open("delegate")
 print rpc.unlock(99999999, config.unlock)
 r = rpc.wallet_list_my_accounts()
 accounts = r["result"]
 for account in accounts :
  if re.match(".*charity.*", account["name"]) :
   if account["delegate_info"] :
    if account["delegate_info"]["pay_balance"] > withdrawfee:
     payout = float(account["delegate_info"]["pay_balance"]) - withdrawfee
     print "%20s -- %20.5f -- %20.5f" % (account["name"], account["delegate_info"]["pay_balance"]/1.0e5, payout/1.0e5)
     print rpc.wallet_delegate_withdraw_pay(account["name"],payouttarget,payout/1.0e5,"auto pay day") 
 print rpc.lock()
