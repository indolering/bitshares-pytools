#!/usr/bin/python3
import bitsharesrpc
import config
from pprint import pprint
from datetime import datetime
from prettytable import PrettyTable
import statistics

numDelegates = 101

if __name__ == "__main__":
 delegatefeeds = []
 feedprice = { }
 currenttime = datetime.utcnow()
 rpc = bitsharesrpc.client(config.url, config.user, config.passwd)
 delegates = rpc.blockchain_list_delegates( 1, numDelegates )
 for top,delegate in enumerate(delegates["result"],1) :
  feeds = rpc.blockchain_get_feeds_from_delegate(delegate["name"])["result"]
  numfeeds = len(feeds)
  validfeed = []
  validfeeds = []
  for feed in feeds :
   feedtime = datetime.strptime(feed["last_update"],"%Y-%m-%dT%H:%M:%S")
   delta    = (currenttime-feedtime)
   if feed[ "asset_symbol" ] not in feedprice : feedprice[ feed["asset_symbol"] ] = [  ]
   feedprice[ feed["asset_symbol"] ].append(feed[ "price" ])
   if delta.total_seconds()/60/60/24 < 1.0 :
    validfeed.append(feed["asset_symbol"])
    validfeeds.append( feed );
  delegatefeeds.append({
                        "name" : str(delegate["name"]),
                        "numValidFeeds":len(validfeed),
                        "feeds": validfeeds,
                        "top": top
                       })

 #data_sorted = sorted(delegatefeeds, key=lambda item: item['numValidFeeds'])
 t = PrettyTable(["asset", "mean", "std", "median"]) 
 t.align                   = 'l'                                                                                                                                                                                                    
 t.border                  = True
 t.float_format['mean']    = ".10"
 t.float_format['median']  = ".10"
 t.float_format['std']     = ".10"
 medianPrice = {}
 for a in feedprice :
  t.add_row([a, statistics.mean(feedprice[a]), statistics.stdev(feedprice[a]), statistics.median(feedprice[a])])
  medianPrice[ a ] = statistics.median(feedprice[a])
 print(t.get_string(sortby="std", reversesort=False))

 ## Large deviation delegates ######################
 t2 = PrettyTable(["delegate","top","numFeeds", "asset"]) 
 t2.align                   = 'l'
 t2.border                  = True
 for p in delegatefeeds : 
  assetstr = ""
  for a in p[ "feeds" ] :
   deviation_from_median = (a[ "price" ]-medianPrice[ a[ "asset_symbol" ]])/medianPrice[ a[ "asset_symbol" ]] * 100
   if deviation_from_median > 1.5 :
    assetstr += "%8s, %11.8f (med%+8.3f%%)\n" % (a["asset_symbol"], a[ "price" ], deviation_from_median)
  if assetstr != "" :
   t2.add_row([p["name"], p["top"], p["numValidFeeds"], assetstr ])
 print("\n\n\nLarge deviation Feeds")
 print(t2.get_string(sortby="top", reversesort=False))

 ## All Statistics #################################
 t3 = PrettyTable(["delegate","top","numFeeds", "asset"]) 
 t3.align                   = 'l'
 t3.border                  = True
 for p in delegatefeeds : 
  deviation_from_median = (a[ "price" ]-medianPrice[ a[ "asset_symbol" ]])/medianPrice[ a[ "asset_symbol" ]] * 100
  assetstr = "\n".join([ "%8s, %11.8f (med%+8.3f%%)" % (a["asset_symbol"], a[ "price" ], deviation_from_median) for a in p[ "feeds" ] ])
  t3.add_row([p["name"], p["top"], p["numValidFeeds"], assetstr ])
 print("\n\n\nAll deviation")
 print(t3.get_string(sortby="top", reversesort=False))
