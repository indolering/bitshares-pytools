#!/usr/bin/python
import bitsharesrpc
import config
import sys

if __name__ == "__main__":
 account = sys.argv[1] 
 rpc = bitsharesrpc.client(config.url, config.user, config.passwd)
 rpc.wallet_open(config.wallet)
 rpc.unlock(999999, config.unlock)
 orders = rpc.wallet_account_order_list(account)
 cancelorders = []
 for i in orders["result"] :
  ret = rpc.wallet_market_cancel_order(i[0])
  assert "error" not in ret, "Error from client: %s" % ret
  print(ret)

  #cancelorders.append(i[0])
 #cancelorders = [i for i in cancelorders]
 #ret = rpc.batch("wallet_market_cancel_order", cancelorders)
 #assert "error" not in ret, "Error from client: %s" % ret

 rpc.lock()
