# -*- coding: utf8 -*-
from bittrex.bittrex import Bittrex, API_V1_1
from termcolor import colored
import json
import time
import os
import sys
import pprint

bittrex_api_version = API_V1_1
fee = 0.25

simulateCryptobuy = 0.0
simulateTotalInBtc = 0.0
simulateBenef = 0.0

def usage():
    if len(sys.argv) != 2:
        print colored("Usage :\t\tpython main.py [Market]\nExample :\tpython main.py XRP", "red")
        sys.exit(-1)

def authBittrex():
    data = json.load(open("config.json"))
    bittrexApi = Bittrex(data['Bittrex param']['my_api_key'], data['Bittrex param']['my_api_secret'], api_version=bittrex_api_version)
    return bittrexApi

def monitor(bittrexApi):
    while True:
        tickSummary = bittrexApi.get_marketsummary("BTC-" + sys.argv[1])
        if tickSummary['success'] == False:
            print colored("get_marketsummary() Failure", 'red')
            return False
        print "get_marketsummary() :\nAsk = " + str(tickSummary['result'][0]['Ask']) + "\nBid = " + str(tickSummary['result'][0]['Bid']) + "\nLast = " + str(tickSummary['result'][0]['Last'])
        print ""
        time.sleep(1)

def getCoinInfo(bittrexApi, coin):
    pp = pprint.PrettyPrinter(indent=4)
    balances = bittrexApi.get_balances()
    for coinLoop in balances['result']:
        if coinLoop['Currency'] == coin:
            return coinLoop
    print colored("Coin not available in your account", "red")
    return False

def maxCoinBuy(availableBtc, pricePerCoin):
    feeCost = availableBtc / pricePerCoin # pricePerCoin : prix pour 1 coin a l'achat
    costInCrypto = feeCost * fee / 100
    maxCoin = feeCost - costInCrypto
    return round(maxCoin, 8)

def buyAtLastPrice(bittrexApi):
    global simulateCryptobuy
    coin = getCoinInfo(bittrexApi, "BTC")
    if coin == False:
        return False
    availableBtc = coin['Available']
    #print bittrexApi.get_marketsummary("BTC-" + sys.argv[1])
    pricePerCoin = bittrexApi.get_marketsummary("BTC-" + sys.argv[1])['result'][0]['Ask']
    maxCoin = maxCoinBuy(availableBtc, pricePerCoin)
    simulateCryptobuy = pricePerCoin
    #print simulateCryptobuy
    #retBuy = bittrexApi.buy_limit("BTC-" + sys.argv[1], maxCoin, pricePerCoin)
    #print retBuy['message']

def simulTrade(bittrexApi):
    global simulateBenef
    lastPrice = bittrexApi.get_marketsummary("BTC-" + sys.argv[1])['result'][0]['Last']
    print "Buying at :" + str(simulateCryptobuy)
    print "Actual price (Last): " + str(sys.argv[1]) + " = " + str(lastPrice)
    simulateBenef = lastPrice - simulateCryptobuy
    if simulateBenef > 0:
        print colored("%.8f" % (simulateBenef), "green")
    elif simulateBenef <= 0:
        print colored("%.8f" % (simulateBenef), "red")

def main():
    usage()
    bittrexApi = authBittrex()
    buyAtLastPrice(bittrexApi)
    while True:
        simulTrade(bittrexApi)
        #time.sleep (1)
    #monitor(bittrexApi)

if __name__ == '__main__':
    main()
