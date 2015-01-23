#!/usr/bin/python
import requests
import json

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
     for b in balance[ "result" ][ 0 ][ 1 ]:
       if b[ 0 ] == asset : return float(b[ 1 ])
     return -1

 def setnetwork(self,d,m) :
     return self.network_set_advanced_node_parameters({"desired_number_of_connections":d, "maximum_number_of_connections":m})

 def orderhistory(self,a,b,l) :
     return self.blockchain_market_order_history(a,b,1,l)

