import requests
import json
import talib
import numpy as np
from datetime import datetime


BASE_URL = 'https://api.binance.com'
PAIRS_ENDPOINT = '/api/v3/exchangeInfo'

def findGoldenCross(pairs):
    for pair in usdts:
        klinesEndpoint = BASE_URL + f'/api/v3/klines?symbol={pair}&interval=1w&limit=500'
        klines = getJson(klinesEndpoint)
        close = np.array(list(map(lambda s: s[4], klines)),dtype='double')
        closingTimestamps = list(map(lambda s: s[6], klines))

        if len(close) == 0:
            continue

        ema20 = talib.EMA(close, timeperiod=20)
        ema55 = talib.EMA(close, timeperiod=55)
        #print(pair)
        #print(ema20)
        #print(ema55)

        weeksPrior = 4
        if len(ema20) >= weeksPrior + 1:
            beginIdx = len(ema20) - weeksPrior
        else:
            beginIdx = 0
        endIdx = len(ema20)
        for i in range(beginIdx, endIdx):
            if(ema55[i-1] > ema20[i-1] and ema55[i] < ema20[i]):
                print(f"golden cross found in pair: {pair} in timestamp {datetime.fromtimestamp(closingTimestamps[i]/1000.0)}")

def getJson(url):
    r = requests.get(url)
    return json.loads(r.text)



exchangeInfoUrl = BASE_URL + PAIRS_ENDPOINT
exchangeInfo =getJson(exchangeInfoUrl)["symbols"]
#print(print(json.dumps(symbols, indent=4, sort_keys=True)))
  
symbols = list(map(lambda s: s["symbol"], exchangeInfo))
#print(symbols)

usdts = list(filter(lambda p: 'USDT' in p, symbols))
#usdts = list(symbols)
#print(usts)

findGoldenCross(usdts)