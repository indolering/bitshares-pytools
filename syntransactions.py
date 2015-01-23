#!/usr/bin/python
from btsrpcapi import *
import config

if __name__ == "__main__":
 rpc = btsrpcapi(config.url, config.user, config.passwd)
 rpc.wallet_open(config.wallet)
 rpc.unlock(999999,config.unlock)
 rpc.lock()
