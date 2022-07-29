import alpaca_trade_api as tradeapi
import random
from alpaca_trade_api.rest import REST, TimeFrame
from datetime import datetime, timedelta
import math

api_key = 'PKU2LXWBDNRDEI6QROXW'
api_secret = '7p4jtrLUMZV2S5e1sQsQoCUSOjxQj6vPQ0WUkKjC'

SEC_KEY = api_secret
PUB_KEY = api_key
BASE_URL = 'https://paper-api.alpaca.markets' # This is the base URL for paper trading
api = tradeapi.REST(key_id= PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL) # For real trading, don't enter a base_url


old_date = datetime.today() - timedelta(3)
old_date_formatted = old_date.strftime ('20%y-%m-%dT%16:00:00Z')
old_date_formatted = str(old_date_formatted)
today = datetime.today()
today_formatted = today.strftime ('20%y-%m-%dT%16:00:00Z')
today_formatted = str(today_formatted)

obv_previous = 0
obv = 0


def get_symbols():
    random.seed(10)
    return_list = []
    assets = api.list_assets(status= 'active')
    for a in assets[:120]:
        if a.exchange == 'NYSE' or a.exchange == 'NASDAQ':
            quote = api.get_bars(a.symbol, TimeFrame.Day, limit = 1)
            if len(quote) > 0:
                if quote[0].c > 5 and quote[0].c < 100:
                    return_list.append(a.symbol)
    return random.sample(return_list, 20)

#print(symb_list)
def sort_second(val):
    return val[1]

def calculate_trade(request):

    symb_list = get_symbols()

    obv_vals = []
    for symb in symb_list:
        market_data = api.get_bars(symb, TimeFrame.Day, old_date_formatted,
                                   today_formatted, limit = 3)
        if len(market_data) == 3:
            #print(market_data[2].v)
            if market_data[1].c > market_data[0].c:
                obv_previous = market_data[1].v
            elif market_data[1].c < market_data[0].c:
                obv_previous = -(market_data[1].v)

            if market_data[2].c > market_data[1].c:
                obv = obv_previous + market_data[2].v
            elif market_data[2].c < market_data[1].c:
                obv = obv_previous - market_data[2].v

            if obv > obv_previous:
                #print(obv, obv_previous, symb)
                pair = []
                pair.append(symb)
                pair.append(obv - obv_previous)
                pair.append(market_data[2].c)
                obv_vals.append(pair)
        
    obv_vals.sort(key=sort_second, reverse=True)
    #print(obv_vals[:5])
    for items in obv_vals[:5]:
        shares = math.floor(100000 / items[2])
        try:
            order = api.submit_order(
                        items[0], # Replace with the ticker of the stock you want to buy
                        shares,
                        'buy',
                        'market', 
                        'opg' # Good 'til cancelled
                )
        except Exception as e:
            message = str(e) + order.status


    return {
        'Message' : message,
        'Success' : 'YES!'
    }

calculate_trade(1)