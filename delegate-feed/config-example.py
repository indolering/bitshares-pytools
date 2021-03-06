################################################################################
## RPC-client connection information (required)
################################################################################
url    = "http://localhost:19988/rpc"
user   = ""
passwd = ""
unlock = ""
wallet = ""

################################################################################
## Delegate Feed Publish Parameters
################################################################################
delegate_list        = [ 
                         "delegate.xeroc",
                         ]
maxAgeFeedInSeconds  = 1200
minValidAssetPrice   = 0.00001
discount             = 0.995
change_min           = 0.5
btc38_trust_level    = 0.7
bter_trust_level     = 1.0
poloniex_trust_level = 0.5
bittrex_trust_level  = 0.5
