import string
import sys
import time
import os
import random
import json
import commands

new_words = []
def make_new_words(count):
    for i in range(count):
        w = ''.join(random.choice(string.ascii_letters).lower() for m in range(10))
        new_words.append(w)


def createAccounts():
    # in my system keosd is runing at 8889 port
    os.system('cleos --wallet-url=http://127.0.0.1:8889 wallet unlock --password=PW5JDUhcbjYFmeW6yYAgpVRZZBH3jRcPr7VWAmcj5Puqaapzutjd8')
    for i in new_words:
        r = os.system('cleos --wallet-url=http://127.0.0.1:8889 create account xingyitoken %s EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV' % i)
        if r is not 0:
            os.system('cleos --wallet-url=http://127.0.0.1:8889 create account xingyitoken %s EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV' % i)

def prepareAccountAndContract(contractname):
    os.system("cleos --wallet-url=http://127.0.0.1:8889 create account eosio " + contractname + " EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV")
    os.system("cleos --wallet-url=http://127.0.0.1:8889 set contract " + contractname + " ~/eos/build/contracts/eosio.token -p " + contractname)


def createAsset(contractname, assetname):
    s = {"issuer":"xingyitoken","maximum_supply":"10000000000000 XYT","can_freeze":0,"can_recall":0,"can_whitelist":0}
    s["issuer"] = contractname
    s["maximum_supply"] = "10000000000000 " + assetname
    s2 = json.dumps(s)
    
    ss = "cleos --wallet-url=http://127.0.0.1:8889 push action " + contractname  + " create " +  "' " + s2 + " '" + " -p " + contractname
    os.system(ss)


def issueToSomeone(contractname, assetname, count, to):
    s = {"to":"eosio","quantity":"10000 XYT","memo":"my-first-transfer"}
    s["to"] = to
    s["quantity"] = str(count) + " " + assetname
    s2 = json.dumps(s)
    
    ss = "cleos --wallet-url=http://127.0.0.1:8889 push action " +  contractname + " issue " +  "' " + s2 + " '" + " -p " + contractname
    os.system(ss)


def transferToSomeone(contractname, from_account, to_account, count, assetname):
    s = {"to":"eosio","quantity":"10000 XYT","memo":"my-first-transfer"}
    s["from"] = from_account
    s["to"] = to_account
    s["quantity"] = str(count) + " " + assetname
    s["memmo"] = "test transfer"
    s2 = json.dumps(s)
    
    ss = "cleos --wallet-url=http://127.0.0.1:8889 push action " + contractname + " transfer " +  "' " + s2 + " '" + " -p " + from_account
    os.system(ss)

def getAccountMemoryUsage(account):
    ss = "cleos --wallet-url=http://127.0.0.1:8889 get account " + account + " -j"
    print ss
    (_, s) = commands.getstatusoutput(ss)
    p = json.loads(s)
    return p['ram_usage']
    

def TestMemoryClaim():
    clients = 1000
    if len(sys.argv) < 2:
        print("contractname assetname")
        exit(-1)
    make_new_words(clients)
    createAccounts()

    contractname = sys.argv[1]
    asset_name = sys.argv[2]

    prepareAccountAndContract(contractname)
    print "after set contract code, memory usage is: " + str(getAccountMemoryUsage(contractname))
    createAsset(contractname, asset_name)
    print "after creating an asset, memory usage is: " + str(getAccountMemoryUsage(contractname))

    #issule 1000 tokens to everyone
    for i in  new_words:
        issueToSomeone(contractname, asset_name, 1000, i)

    print("after issue to %d clients, memory usage is: %d" % (clients, getAccountMemoryUsage(contractname)))

    #transfer back to the issuer, aka claim
    for i in  new_words:
        transferToSomeone(contractname, i, contractname, 1000, asset_name)
    
    print("after claimed %d clients's token, memory usage is: %d" %(clients, getAccountMemoryUsage(contractname)))
    


if __name__ == "__main__":
    TestMemoryClaim()
