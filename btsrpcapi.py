#!/usr/bin/python

import requests
import json

class btsrpcapi :
 def __init__(self, url, user, pwd) :
     self.auth    = (user,pwd)
     self.url     = url
     self.headers = {'content-type': 'application/json'}
   
 def rpcexec(self,payload) :
     try :
      response = requests.post(self.url, data=json.dumps(payload), headers=self.headers, auth=self.auth)
      return json.loads(response.text)
     except :
      return -1
     
 def getstatus(self) :
     return self.rpcexec({
        "method": "get_info",
        "params": [],
        "jsonrpc": "2.0",
        "id": 0
     })
     
 def walletopen(self,name) :
     return self.rpcexec({
         "method": "wallet_open",
         "params": [name],
         "jsonrpc": "2.0",
         "id": 0
     })

 def unlock(self,key) :
     return self.rpcexec({
         "method": "wallet_unlock",
         "params": ["99999999999", key],
         "jsonrpc": "2.0",
         "id": 0
     })

 def lock(self) :
     return self.rpcexec({
         "method": "wallet_lock",
         "params": [],
         "jsonrpc": "2.0",
         "id": 0
     })
 def approvedelegate(self,name) :
     return self.rpcexec({
         "method": "wallet_approve_delegate",
         "params": [name, "1"],
         "jsonrpc": "2.0",
         "id": 0
     })

 def unapprovedelegate(self,name) :
     return self.rpcexec({
         "method": "wallet_approve_delegate",
         "params": [name, "0"],
         "jsonrpc": "2.0",
         "id": 0
     })

 def walletallgetaccounts(self) :
     return self.rpcexec({
         "method": "wallet_list_accounts",
         "params": [],
         "jsonrpc": "2.0",
         "id": 0
     })

 def walletgetaccounts(self) :
     return self.rpcexec({
         "method": "wallet_list_my_accounts",
         "params": [],
         "jsonrpc": "2.0",
         "id": 0
     })

 def publishslate(self, delegate, payee) :
     return self.rpcexec({
         "method": "wallet_publish_slate",
         "params": [delegate, payee],
         "jsonrpc": "2.0",
         "id": 0
     })
