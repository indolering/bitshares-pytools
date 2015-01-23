#!/usr/bin/python
from btsrpcapi import *
import config

if __name__ == "__main__":
 rpc = btsrpcapi(config.url, config.user, config.passwd)
 rpc.info()
 rpc.wallet_open("delegate")
 rpc.unlock(9999999, config.unlock)
 rpc.setnetwork(120,200)
 rpc.wallet_delegate_set_block_production("ALL","true")
