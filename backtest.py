import alpaca_trade_api as tradeapi
import numpy as np 
import time
from alpaca_trade_api.rest import REST, TimeFrame
from datetime import datetime, timedelta
import pandas as pd 
import math

api_key = 'PK4IRABDHR69FNG681E9'
api_secret = 'Qa4KAOR2tivzExV89H60p8p524bqj4ALOv7uQVVS'

SEC_KEY = api_secret
PUB_KEY = api_key
BASE_URL = 'https://paper-api.alpaca.markets' # This is the base URL for paper trading
api = tradeapi.REST(key_id= PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL) # For real trading, don't enter a base_url

startBal = 500
balance = startBal

pos_held = False
days = 200 #6months  
symb = 'BB'

old_date = datetime.today() - timedelta(90)
old_date_formatted = old_date.strftime ('20%y-%m-%dT%4:00:00Z')
old_date_formatted = str(old_date_formatted)

recent_date = datetime.today() - timedelta(2)
recent_date_formated = recent_date.strftime ('20%y-%m-%dT%4:00:00Z')
recent_date_formated = str(recent_date_formated)

obv = 0
obv_previous = 1
obv_list = []
sells = 0
buys = 0
shares = 0

#previous_market = api.get_bars(symb, TimeFrame.Day, todays_date_formatted,limit=1)
obv_previous = 0
# for i in range(1,30):
    # the_date = todays_date + timedelta(i)
    # the_date_formatted = the_date.strftime ('20%y-%m-%dT%16:00:00Z')
    # the_date_formatted = str(the_date_formatted)

    # tomorrow = todays_date + timedelta(i + 1)
    # tommorrw_formatted = tomorrow.strftime ('20%y-%m-%dT%9:45:00Z')
    # tommorrw_formatted = str(tommorrw_formatted)

    #clearprint(todays_date_formatted)
market_data = api.get_bars(symb, TimeFrame.Day, old_date_formatted, recent_date_formated, limit=90)
    #tommorow_market = api.get_bars(symb, TimeFrame.Day, tommorrw_formatted,limit=1)
     # Pull market data from the past 60x minutes
    
    #print('todays', todays_date_formatted)
    #print(market_data)
days_data = []
for bar in market_data:
    data = []
    data.append(bar.c)
    data.append(bar.v)
    data.append(bar.t)
    data.append(bar.o)
    days_data.append(data)


for i in range(1, len(days_data) - 2):
    if days_data[i][0] > days_data[i-1][0]:
        #print('good')
        obv = obv_previous + days_data[i][1]
    elif days_data[i][0] < days_data[i-1][0]:
        obv = obv_previous - days_data[i][1]
        #print('bad')
    
    print('obv: ', obv)
    print('previous obv: ', obv_previous)
    print(days_data[i + 1][2])
    if days_data[i][0] > days_data[i-1][0]:
        shares_to_buy = math.floor(balance / days_data[i + 1][3])
        print('Bought ', shares_to_buy, 'at ', '$',  days_data[i + 1][3])
        balance -= days_data[i + 1][3] * shares_to_buy
        if shares_to_buy > 0:
            cost = days_data[i + 1][3] * shares_to_buy
        pos_held = True
        buys += shares_to_buy
        shares += shares_to_buy

        #if days_data[i + 1][0] < days_data[i + 1][3]:
        print('Sold ',  shares, 'at ', '$',  days_data[i + 1][0])
        print('cost: ', cost)
        sold = 0
        while shares > 0:
        #print("Sell")
            sold += days_data[i + 1][0]
            balance += days_data[i + 1][0]
            pos_held = True
            sells += 1
            shares -= 1
        print('sold for: ', sold)



        #print(balance)clear
        # #print('trigger')
        # if (obv < 0 and obv_previous) > 0 or (obv < 0 and obv_previous < 0):
        #     difference = abs((obv / obv_previous) - 1)
        # else: 
        #     difference = (obv / obv_previous) - 1
        # print(difference, 'gain')
        # if difference >= .3:
        #     #print("Buy")
        #     balance -= market_data[0].c * 15
        #     pos_held = True
        #     buys += 15
        #     shares += 15
        # elif difference > .15:
        #     #print("Buy")
        #     balance -= market_data[0].c * 8
        #     pos_held = True
        #     buys += 8
        #     shares += 8
        # elif difference >= .05:
        #     #print("Buy")
        #     balance -= market_data[0].c * 5
        #     pos_held = True
        #     buys += 3
        #     shares += 3


        
        
    # elif obv <= obv_previous and shares > 0:
    #     print('bad')
    #     print('Sold: ', market_data[0].o)
    #     print('Shares sold: ', shares)
    #     print('Tommorows Close: ', tommorow_market[0].c)
    #     while shares > 0:
    #     #print("Sell")
    #         balance += market_data[0].o
    #         pos_held = True
    #         sells += 1
    #         shares -= 1
        
        # if (obv < 0 and obv_previous) > 0 or (obv < 0 and obv_previous < 0):
        #     difference = abs((obv / obv_previous) - 1)
        # else: 
        #     difference = obv / obv_previous

        # print(difference, 'loss')
        # if difference  > .5 and shares >= 15:
        #     #print("Sell")
        #     balance += market_data[0].c * 15
        #     pos_held = True
        #     sells += 15
        #     shares -= 15
        # elif difference > .3 and shares >= 8:
        #     #print("Sell")
        #     balance += market_data[0].c * 8
        #     pos_held = True
        #     sells += 8
        #     shares -= 8
        # else:
        #     while shares > 3:
        #         #print("Sell")
        #         balance += market_data[0].c
        #         pos_held = True
        #         sells += 1
        #         shares -= 1
    

    obv_list.append(obv)
    #obv_list.append(todays_date_formatted)
    previous_market = market_data
    obv_previous = obv
    print('Bal', balance)
    time.sleep(0.01)
    print('\n')
while shares > 0:
    #print("Sell")
    balance += market_data[0].c
    pos_held = True
    sells += 1
    shares -= 1

    #print("")
print("Buys: " + str(buys))
print("Sells: " + str(sells))
print(balance)
print("Profit from algorithm: " + str(balance - startBal))
if balance > startBal:
    print('% inc: ', balance/startBal - 1   )
elif (balance < startBal):
    print('%loss: ', 1 - balance/startBal)
#print(obv_list)


    
     
    



        