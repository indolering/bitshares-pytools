################################################################################
## RPC-client connection information (required)
################################################################################
url    = "http://localhost:19988/rpc"
user   = ""
passwd = ""
unlock = ""
wallet = "default"

################################################################################
## Settings for the payouts
################################################################################
accountname  = "delegate.xeroc"    # delegate name
exchangename = "exchange.xeroc"    # account name in which dex operations are performed
payoutname   = "payouts.xeroc"     # account name for payouts (all assets)

################################################################################
## Settings for the payouts
################################################################################
partition    = {
                   "USD" : .5,      # exchange 50% into USD
                   "BTS" : .5,      # do not exchange 50% .. keep BTS
               }
spread       = 0.05 # 0.0: put ask at price feed   0.05: 5% below pricefeed (wait for someone to sell into you)
txfee        = 0.1  # BTS tx fee
withdrawlimit= 100  # keep 100 BTS in your exchange account
btsprecision = 1e5  # should always be 1e5 :)
