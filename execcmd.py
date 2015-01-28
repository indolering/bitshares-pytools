#!/usr/bin/python
import bitsharesrpc
import config
import sys
from pprint import pprint 

if __name__ == "__main__":
     rpc = bitsharesrpc.client(config.url, config.user, config.passwd)
     cmd = sys.argv[1] 
     print list(sys.argv[2:])
     pprint((rpc.rpcexec({
       "method": cmd,
       "params": list(sys.argv[2:]),
       "jsonrpc": "2.0",
       "id": 0
       })))
