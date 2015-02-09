#!/usr/bin/python
import bitsharesrpc
import config
from pprint import pprint

accountname  = "delegate.xeroc"
exchangename = "exchange.xeroc"
payoutname   = "payouts.xeroc"
partition    = {
                   "EUR" : .5,
                   "BTS" : .5,
               } ## BTS has to be last
spread       = 0.00 # 0.0: put ask at price feed   0.05: 5% below pricefeed
txfee        = 0.1 # BTS
btsprecision = 1e5
withdrawlimit= 100

if __name__ == "__main__":
 assert sum(partition.values()) == 1.0, "Partition must sum up to 1.0 but is %f" %sum(partition.values())

 rpc = bitsharesrpc.client(config.url, config.user, config.passwd)
 ret = rpc.wallet_open(config.wallet)
 assert "error" not in ret, "Error from client: %s" % ret
 ret = rpc.unlock(999999,config.unlock)
 assert "error" not in ret, "Error from client: %s" % ret

 # Withdraw delegate pay #############################################
 print("-"*80)
 print("| Withdrawing delegate pay")
 print("-"*80)
 account = rpc.wallet_get_account(accountname)["result"]
 assert "delegate_info" in account, "Account %s not registered as delegate" % accountname
 if float(account["delegate_info"]["pay_balance"]) < withdrawlimit*btsprecision :
  print "Not enough pay to withdraw yet!"
 else :
  payout = float(account["delegate_info"]["pay_balance"]) - txfee*btsprecision
  print "Withdrawing %10.5f BTS from %s to %s" % (account["delegate_info"]["pay_balance"]/btsprecision,account["name"], exchangename)
  ret = rpc.wallet_delegate_withdraw_pay(account["name"],exchangename,payout/btsprecision, "auto pay day") 
  assert "error" not in ret, "Error from client: %s" % ret
  ## wait
  rpc.wait_for_block()
  rpc.wait_for_block()

 # Exchange ##########################################################
 print("-"*80)
 print("| Exchanging delegate pay")
 print("-"*80)
 amount = rpc.market.get_balance( exchangename, 0 ) - len(partition)*txfee*2
 for asset in partition : 
  percent = partition[asset]
  if asset == "BTS" : 
   amount += txfee # no need for fee
   continue
  feedprice = rpc.blockchain_market_status( asset , "BTS" )["result"]["current_feed_price"]
  askprice = feedprice / (1-spread)
  quant    = amount * percent
  if quant < 0 : continue
  print "wallet_market_submit_ask %s %f %s %f %s" %(exchangename,  quant, "BTS", askprice, asset)
  #ret = rpc.wallet_market_submit_ask(exchangename, quant, "BTS", askprice, asset)
  ret = rpc.market.ask_limit(exchangename, quant, "BTS", asset, askprice, confirm=False)
 assert "error" not in ret, "Error from client: %s" % ret

 ## wait
 #rpc.wait_for_block()
 #rpc.wait_for_block()

 # Transfer to payoutname ############################################
 print("-"*80)
 print("| Sending funds to payout account")
 print("-"*80)
 for asset in partition : 
  assetid = rpc.blockchain_get_asset(asset)["result"]["id"]
  amount = rpc.market.get_balance( exchangename, assetid)
  if asset == "BTS" : continue
  if amount > 0.0 :
   print "Sending %10.5f %s from %s to %s" % (amount,asset,exchangename,payoutname)
   ret = rpc.wallet_transfer(amount, asset, exchangename, payoutname, "auto payex")
   assert "error" not in ret, "Error from client: %s" % ret

 # Transfer to payoutname ############################################
 print("-"*80)
 print("| Sending BTS to payout account")
 print("-"*80)
 assetid   = rpc.blockchain_get_asset("BTS")["result"]["id"]
 amount    = rpc.market.get_balance( exchangename, assetid) - 10*txfee  # keep 10x txfee as reserve
 if amount > txfee :
  print "Sending %10.5f BTS from %s to %s" % (amount,exchangename,payoutname)
  ret = rpc.wallet_transfer(amount, asset, exchangename, payoutname, "auto payex")
  assert "error" not in ret, "Error from client: %s" % ret

 # Lock wallet #######################################################
 rpc.lock()
