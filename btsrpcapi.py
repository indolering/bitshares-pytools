#!/usr/bin/python
import requests
import json
import time

class btsrpc(object) :
 def __init__(self, url, user, pwd) :
     self.auth    = (user,pwd)
     self.url     = url
     self.headers = {'content-type': 'application/json'}

 def rpcexec(self,payload) :
     try: 
         response = requests.post(self.url, data=json.dumps(payload), headers=self.headers, auth=self.auth)
         return json.loads(response.text)
     except:

         raise Exception("Unkown error executing RPC call!")
 def __getattr__(self, name) :
     def method(*args):
         r = self.rpcexec({
             "method": name,
             "params": args,
             "jsonrpc": "2.0",
             "id": 0
         })
         if "error" in r:
             raise Exception(r["error"])
         return r
     return method

class btsrpcapi(btsrpc) :
 def __init__(self, url, user, pwd) :
     btsrpc.__init__(self, url, user, pwd)

 def getassetbalance(self,name,asset) :
     balance = self.wallet_account_balance(name)
     if len(balance[ "result" ])==0 : return 0.0
     for b in balance[ "result" ][ 0 ][ 1 ]:
       if b[ 0 ] == asset : return float(b[ 1 ])
     return -1

 def setnetwork(self,d,m) :
     return self.network_set_advanced_node_parameters({"desired_number_of_connections":d, "maximum_number_of_connections":m})

 def get_precision(self, asset):
     response = self.blockchain_get_asset(asset)
     return float(response["result"]["precision"])

 def orderhistory(self,a,b,l) :
     return self.blockchain_market_order_history(a,b,1,l)

 def cancel_all_orders(self, account, quote, base):
     cancel_args = self.get_all_orders(account, quote, base)
     #response = self.request("batch", ["wallet_market_cancel_order", [cancel_args[0]] ])
     for i in cancel_args[0] :
         response = self.request("wallet_market_cancel_order", [i])
     return cancel_args[1]

 def wait_for_block(self):
     response = self.get_info()
     blocknum = response["result"]["blockchain_head_block_num"]
     while True:
         time.sleep(0.1)            
         response = self.get_info()
         blocknum2 = response["result"]["blockchain_head_block_num"]
         if blocknum2 != blocknum:
             return

 def ask_at_market_price(self, name, amount, base, quote, confirm=False) :
     last_fill      = -1
     response       = self.blockchain_market_order_book(quote, base)
     quotePrecision = self.get_precision(quote)
     basePrecision  = self.get_precision(base)
     orders = []
     for order in response["result"][0]: # bid orders
         order_price  = float(order["market_index"]["order_price"]["ratio"])*(basePrecision / quotePrecision) 
         order_amount = float(order["state"]["balance"]/quotePrecision) / order_price  # denoted in BASE
         if amount >= order_amount : # buy full amount
           orders.append([name, order_amount, base, order_price, quote])
           amount -= order_amount
         elif amount < order_amount: # partial
           orders.append([name, amount, base, order_price, quote])
           break
     for o in orders :
         print( "Selling %15.8f %s for %12.8f %s @ %12.8f" %(o[1], o[2], o[1]*o[3], o[4], o[3]) )
     orders = [ i for i in orders ]
     if not confirm or self.query_yes_no( "I dare you confirm the orders above: ") :
         return self.batch("ask", orders)

 def bid_at_market_price(self, name, amount, base, quote, confirm=False) :
     last_fill      = -1
     response       = self.blockchain_market_order_book(quote, base)
     quotePrecision = self.get_precision(quote)
     basePrecision  = self.get_precision(base)
     orders = []
     for order in response["result"][1]: # ask orders
         order_price  = float(order["market_index"]["order_price"]["ratio"])*(basePrecision / quotePrecision) 
         order_amount = float(order["state"]["balance"]/quotePrecision) / order_price  # denoted in BASE
         if amount >= order_amount : # buy full amount
           orders.append([name, order_amount, base, order_price, quote])
           amount -= order_amount
         elif amount < order_amount: # partial
           orders.append([name, amount, base, order_price, quote])
           break
     for o in orders :
         print( "Buying %15.8f %s for %12.8f %s @ %12.8f" %(o[1], o[2], o[1]*o[3], o[4], o[3]) )
     orders = [ i for i in orders ]
     if not confirm or self.query_yes_no( "I dare you confirm the orders above: ") :
         return self.batch("bid", orders)
