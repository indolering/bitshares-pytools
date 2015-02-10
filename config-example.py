################################################################################
## RPC-client connection information (required)
################################################################################
url    = "http://127.0.0.1:19988/rpc"
user   = 'username'
passwd = 'pwd'
unlock = "unlockPwd"
wallet = "default"

################################################################################
## Trusted delegates for slate (required for delegate-slate)
################################################################################
slatedelegate = "delegate.xeroc"
slatepayee    = "payouts.xeroc"
trusted = [
  "a.delegate.charity",
  "alecmenconi",
  "angel.bitdelegate",
  "argentina-marketing.matt608",
  "b.delegate.charity",
  "backbone.riverhead",
  "bdnoble",
  "bitcoiners",
  "bitcube",
  "bitsuperlab.gentso",
  "bm.payroll.riverhead",
  "bts.fordream",
  "btstools.digitalgaia",
  "calabiyau",
  "clout-delegate1",
  "crazybit",
  "d1.yunbi",
  "d2.yunbi",
  "dacx.baozou",
  "del.coinhoarder",
  "del0.cass",
  "dele-puppy",
  "delegate-clayop",
  "delegate-dev1.btsnow",
  "delegate-dev2.btsnow",
  "delegate-dev3.btsnow",
  "delegate-dev4.btsnow",
  "delegate.baozi",
  "delegate.charity",
  "delegate.ihashfury",
  "delegate.jabbajabba",
  "delegate.liondani",
  "delegate.nathanhourt.com",
  "delegate.rgcrypto",
  "delegate.xeldal",
  "delegate1.john-galt",
  "dev-metaexchange.monsterer",
  "dev.bitsharesblocks",
  "dev.sidhujag",
  "dev0.nikolai",
  "developer.vikram",
  "elmato",
  "forum.lottocharity",
  "fund.bitsharesbreakout",
  "fuzzy.beyondbitcoin",
  "happyshares",
  "jcalfee1-developer-team.helper.liondani",
  "luckybit",
  "maqifrnswa",
  "market.cn.group101",
  "market.cn.group101",
  "marketing.methodx",
  "martin-38ptswarrior-raum",
  "media-delegate",
  "media.bitscape",
  "mr.agsexplorer",
  "paid-delegate-cutoff.misc.nikolai",
  "provisional.bitscape",
  "spartako",
  "stan.delegate.xeldal",
  "testz",
  "titan.crazybit",
  "triox-delegate",
  "valzav.payroll.testz",
  "wackou.digitalgaia",
  "www.bts-hk",
  "delegate.verbaltech",
  "dev-pc.bitcube",
]

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
