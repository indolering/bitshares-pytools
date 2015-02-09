################################################################################
## RPC-client connection information (required)
################################################################################
url    = "http://127.0.0.1:19988/rpc"
user   = 'username'
passwd = 'pwd'
unlock = "unlockPwd"
wallet = "default"

################################################################################
## Delegate Feed Publish Parameters (required only for delegate-feed/bts-feed
################################################################################
delegate_list        = [ "delegate.xeroc",
                         "a.delegate.xeroc",
                         "b.delegate.xeroc",
                         "delegate.charity",
                         "a.delegate.charity",
                         "c.delegate.charity"],
payaccount           = "delegate.xeroc",
maxAgeFeedInSeconds  = 1200,
minValidAssetPrice   = 0.00001,
discount             = 0.995,
change_min           = 0.5,
btc38_trust_level    = 1.0,
bter_trust_level     = 1.0,
poloniex_trust_level = 0.5,
bittrex_trust_level  = 0.5
