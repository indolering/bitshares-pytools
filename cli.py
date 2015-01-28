#!/usr/bin/python
import bitsharesrpc,config,json

rpc = bitsharesrpc.client(config.url, config.user, config.passwd)
while 1:
 cmd = raw_input(">> ").split()
 print(json.dumps(rpc.rpcexec({
            "method": cmd[0],
            "params": list(cmd[1:]),
            "jsonrpc": "2.0",
            "id": 0
            }), indent=4))
