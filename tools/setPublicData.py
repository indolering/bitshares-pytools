#!/usr/bin/python
import bitsharesrpc
import config

#######################################
#publicData = {
# "website" : "http://www.bitshares-charity.org",
# "delegate" : {
#        "description": "BitShares Charity",
#        "proposal" : "non-profit for charity",
#        "country" : "de",
#        "location" : "LA/US",
#        "specs" : "VPS-2GB RAM",
#        "payout" : "http://www.charity-delegate.org",
#        "owner" : "xeroc",
#        "handle" : "xeroc",
#        "vote" : {
#                    "also"    : ["delegate.charity", "a.delegate.charity", "b.delegate.charity", "c.delegate.charity"],
#                 },
#        "role" : 4
#  },
# "email" : "contact@charity-delegate.org",
# "gpg" : "0xDA03EB3C2A49AD7D61289168F2538A4B282D6238"
#}
#delegates = [ 
#             "delegate.charity",
#             "a.delegate.charity",
#             "b.delegate.charity",
#             "c.delegate.charity",
#             "d.delegate.charity",
#             "e.delegate.charity",
#             "f.delegate.charity",
#            ]
#payee   = "payouts.charity"
#payrate = 3
#########################################
publicData = {
 "website" : "www.xeroc.org",
 "delegate" : {
        "description": "reliable backbone and commited long-term supporter",
        "proposal" : "user/delegate support, Q&A",
        "country" : "de",
        "location" : "LA/US",
        "specs" : "VPS-2GB RAM",
        "owner" : "xeroc",
        "handle" : "xeroc",
        "vote" : {
                    "also"    : "delegate.charity"
                 },
        "role" : 3
  },
 "email" : "mail@xeroc.org",
 "xmpp" : "",
 "gpg" : "0xDA03EB3C2A49AD7D61289168F2538A4B282D6238"
}
delegates = [ 
             "delegate.xeroc"
            ]
payee = "payouts.xeroc"
payrate = 3
#########################################

if __name__ == "__main__":
 rpc = bitsharesrpc.client(config.url, config.user, config.passwd)
 rpc.wallet_open("delegate")
 rpc.unlock(999999,config.unlock)
 for d in delegates :
     #### Load existing tags
     onchain = rpc.blockchain_get_account(d)["result"]["public_data"]
     #### Merge tags
     newData = {key: value for (key, value) in (onchain.items() + publicData.items())}
     #### update on chain tags
     print rpc.wallet_account_update_registration(d, payee, newData, payrate)
 rpc.lock()
