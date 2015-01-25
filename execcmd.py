#!/usr/bin/python
import bitsharesrpc
import config
import sys
from pprint import pprint 

if __name__ == "__main__":
     rpc = bitsharesrpc.client(config.url, config.user, config.passwd)
     cmd = sys.argv[1] 
     data = sys.argv[2:] 
     pprint((rpc.rpcexec({
       "method": cmd,
       "params": list(data),
       "jsonrpc": "2.0",
       "id": 0
       })))
