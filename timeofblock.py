#!/usr/bin/python
from datetime import datetime,timedelta
from btsrpcapi import *
import config
import sys

confirmationTime = timedelta( seconds=10 )

if __name__ == "__main__":
     rpc = btsrpcapi(config.url, config.user, config.passwd)
     status = rpc.info()
     blockhead = status[ "result" ][ "blockchain_head_block_num" ]
     block = rpc.blockchain_get_block(blockhead)
     nowtime = datetime.strptime(block[ "result" ][ "timestamp" ],"%Y-%m-%dT%H:%M:%S")
     blockNum = int(sys.argv[ 1 ])
     print("block %d to appear in <= %s" % (blockNum,str(confirmationTime*(blockNum-blockhead))))
     print("UTC time: %s" % str(nowtime+confirmationTime*(blockNum-blockhead)))
