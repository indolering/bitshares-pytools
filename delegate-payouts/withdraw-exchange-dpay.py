#!/usr/bin/python
import bitsharesrpc
import config

if __name__ == "__main__":
 assert sum(config.partition.values()) == 1.0, "config.partition must sum up to 1.0 but is %f" %sum(config.partition.values())

 rpc = bitsharesrpc.client(config.url, config.user, config.passwd)
 rpc.wallet_open(config.wallet)
 rpc.unlock(999999,config.unlock)

 # Withdraw delegate pay #############################################
 print("-"*80)
 print("| Withdrawing delegate pay")
 print("-"*80)
 account = rpc.wallet_get_account(config.accountname)["result"]
 assert "delegate_info" in account, "Account %s not registered as delegate" % config.accountname
 if float(account["delegate_info"]["pay_balance"]) < config.withdrawlimit*config.btsprecision :
  print "Not enough pay to withdraw yet!"
 else :
  payout = float(account["delegate_info"]["pay_balance"]) - config.txfee*config.btsprecision
  print "Withdrawing %10.5f BTS from %s to %s" % (account["delegate_info"]["pay_balance"]/config.btsprecision,account["name"], config.exchangename)
  ret = rpc.wallet_delegate_withdraw_pay(account["name"],config.exchangename,payout/config.btsprecision, "auto pay day") 
  ## wait
  rpc.wait_for_block()
  rpc.wait_for_block()

 # Exchange ##########################################################
 print("-"*80)
 print("| Exchanging delegate pay")
 print("-"*80)
 amount = rpc.market.get_balance( config.exchangename, 0 ) - len(config.partition)*config.txfee*2
 for asset in config.partition : 
  percent = config.partition[asset]
  if asset == "BTS" : 
   amount += config.txfee # no need for fee
   continue
  feedprice = rpc.blockchain_market_status( asset , "BTS" )["result"]["current_feed_price"]
  askprice = feedprice / (1-config.spread)
  quant    = amount * percent
  if quant < 0 : continue
  print "wallet_market_submit_ask %s %f %s %f %s" %(config.exchangename,  quant, "BTS", askprice, asset)
  #ret = rpc.wallet_market_submit_ask(config.exchangename, quant, "BTS", askprice, asset)
  rpc.market.ask_limit(config.exchangename, quant, "BTS", asset, askprice, confirm=False)

 ## wait
 #rpc.wait_for_block()
 #rpc.wait_for_block()

 # Transfer to config.payoutname ############################################
 print("-"*80)
 print("| Sending funds to payout account")
 print("-"*80)
 for asset in config.partition : 
  assetid = rpc.blockchain_get_asset(asset)["result"]["id"]
  amount = rpc.market.get_balance( config.exchangename, assetid)
  if asset == "BTS" : continue
  if amount > 0.0 :
   print "Sending %10.5f %s from %s to %s" % (amount,asset,config.exchangename,config.payoutname)
   ret = rpc.wallet_transfer(amount, asset, config.exchangename, config.payoutname, "auto payex")

 ## wait
 rpc.wait_for_block()

 # Transfer to config.payoutname ############################################
 print("-"*80)
 print("| Sending BTS to payout account")
 print("-"*80)
 assetid   = rpc.blockchain_get_asset("BTS")["result"]["id"]
 amount    = rpc.market.get_balance( config.exchangename, assetid) - config.txfee - config.withdrawlimit  # keep 10x config.txfee as reserve
 if amount > 0.0 :
  print "Sending %10.5f BTS from %s to %s" % (amount,config.exchangename,config.payoutname)
  ret = rpc.wallet_transfer(amount, "BTS", config.exchangename, config.payoutname, "auto payex")

 # Lock wallet #######################################################
 rpc.lock()
