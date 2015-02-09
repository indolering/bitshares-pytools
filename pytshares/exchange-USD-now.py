#!/usr/bin/python
import bitsharesrpc
import config
from pprint import pprint

accountname = "payouts.xeroc"
amount = "ALL"  # BTS
txfee = 0.1 # BTS

if __name__ == "__main__":
 rpc = bitsharesrpc.client(config.url, config.user, config.passwd)
 rpc.info()
 rpc.wallet_open(config.wallet)
 rpc.unlock(999999,config.unlock)

 ## Get Balance
 if amount == "ALL" : 
  amount = rpc.getassetbalance( accountname, 0 ) / 1e5 - txfee

 ## Get Price
 orders = rpc.blockchain_market_order_book( "USD", "BTS", 100 )
 offers = []
 for os in orders[ "result" ] :
  for o in os :
   if o[ "type" ] == "bid_order" :
    price = float(o[ "market_index" ][ "order_price" ][ "ratio" ]) * 10
    volume = float(o[ "state" ][ "balance" ]) * 10 / 1e5
    offers.append( [ price, volume ])
 offers_sorted = sorted(offers, reverse=1, key=lambda o:o[1])

 mySum = 0.0
 for i in offers_sorted :
  mySum+=i[ 1 ]
  quant = min( [  i[ 1 ]  , amount ] )
  price = i[ 0 ]
  print "wallet_market_submit_ask %s %f %s %f %s" %(accountname,  quant, "BTS", price, "USD")
  #print rpc.wallet_market_submit_ask(accountname, quant, "BTS", price, "USD")
  amount = amount - quant - txfee
  if amount <= 0.0 :
   break
 rpc.lock()
