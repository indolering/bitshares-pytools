## URL to RPC API of client
url    = "http://10.0.0.16:19988/rpc"

## User as defined with --rpcuser=test or BitShares config file
user   = 'username'

## User as defined with --rpcpassword=test or BitShares config file
passwd = 'password'

## Wallet name ( default: default :) )
wallet = "default"

## Unlock passphrase for the wallet
unlock = ""

## Delegate for which to publish a slate
delegate = "delegate.xeroc"

## Delegate which pays for the slate broadcast transaction
payee    = "payouts.xeroc"
## NOTE: the private keys for both, "delegate" and "payee", must be in
##       available in the wallet!

## List of trusted delegates
trusted = [
	"a.delegate.charity",
	"alecmenconi",
	"angel.bitdelegate",
	"b.delegate.charity",
	"backbone.riverhead",
	"bdnoble",
	"bitcoiners",
	"bitcube",
	"bitsuperlab.gentso",
	"clout-delegate1",
	"crazybit"
	"del.coinhoarder",
	"dele-puppy",
	"delegate.baozi",
	"delegate.charity",
	"delegate.jabbajabba",
	"delegate.liondani",
	"delegate.svk31",
	"delegate.xeldal",
	"delegate1.john-galt",
	"forum.lottocharity",
	"happyshares",
	"luckybit",
	"maqifrnswa",
	"mr.agsexplorer",
	"skyscraperfarms",
	"spartako",
	"testz",
	"wackou.digitalgaia",
]
