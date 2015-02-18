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
 tableAssets = PrettyTable(["asset", "mean", "std", "median"]) 
 tableAssets.align                   = 'l'                                                                                                                                                                                                    
 tableAssets.border                  = True
 tableAssets.float_format['mean']    = ".10"
 tableAssets.float_format['median']  = ".10"
 tableAssets.float_format['std']     = ".10"
 medianPrice = {}
 for a in feedprice :
  tableAssets.add_row([a, statistics.mean(feedprice[a]), statistics.stdev(feedprice[a]), statistics.median(feedprice[a])])
  medianPrice[ a ] = statistics.median(feedprice[a])
 print(tableAssets.get_string(sortby="std", reversesort=False))

 ## Large deviation delegates ######################
 tableLargeDev = PrettyTable(["delegate","top","numFeeds", "asset"]) 
 tableLargeDev.align                   = 'l'
 tableLargeDev.border                  = True
 for p in delegatefeeds : 
  assetstr = ""
  for a in p[ "feeds" ] :
   deviation_from_median = (a[ "price" ]-medianPrice[ a["asset_symbol"]])/medianPrice[ a["asset_symbol"]] * 100
   if deviation_from_median > 1.5 :
    assetstr += "%8s, %11.8f (med%+8.3f%%)\n" % (a["asset_symbol"], a[ "price" ], deviation_from_median)
  if assetstr != "" :
   tableLargeDev.add_row([p["name"], p["top"], p["numValidFeeds"], assetstr ])
 print("\n\n\nLarge deviation Feeds")
 print(tableLargeDev.get_string(sortby="top", reversesort=False))

 ## All Statistics #################################
 tableAll = PrettyTable(["delegate","top","numFeeds", "asset"]) 
 tableAll.align                   = 'l'
 tableAll.border                  = True
 for p in delegatefeeds : 
  assetstr = ""
  assetstr = "\n".join([ "%8s, %11.8f (med%+8.3f%%)" % (a["asset_symbol"], a[ "price" ], 100*(a[ "price" ]-medianPrice[ a[ "asset_symbol" ]])/medianPrice[ a[ "asset_symbol" ]]) for a in p[ "feeds" ] ])
  tableAll.add_row([p["name"], p["top"], p["numValidFeeds"], assetstr ])
 print("\n\n\nAll deviation")
 print(tableAll.get_string(sortby="top", reversesort=False))
