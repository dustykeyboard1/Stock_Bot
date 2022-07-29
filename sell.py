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
api = tradeapi.REST(key_id= PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)


def sell_stock(request):

    positions = api.get_activities('FILL')
    for spot in positions:
        try:
            order = api.submit_order(
                        spot.symbol, # Replace with the ticker of the stock you want to buy
                        spot.qty,
                        'sell',
                        'market', 
                        'cls' # Good 'til cancelled
            )
        except Exception as e:
            message = str(e) + order.status
sell_stock(1)