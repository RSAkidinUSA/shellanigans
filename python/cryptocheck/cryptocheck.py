#!/usr/bin/python3
import requests
import random
import time
import sys

API_URL = "https://api.gdax.com"
crypto_list = ['BTC', 'LTC', 'ETH', 'BTH']
region_dict = { 'US' : {'symbol' : '$', 'string' : 'USD'}, \
				'UK' : {'symbol' : '£', 'string' : 'GPB'}, \
				'EU' : {'symbol' : '€', 'string' : 'EUR'} }

def _get_price(crypto='BTC', region='US'):
	# determine exchange symbol for currency and region
	exchange_symbol = crypto + '-' + region_dict[region]['string']
	region_symbol = region_dict[region]['symbol']
	
	r = requests.get(API_URL + '/products/' + exchange_symbol + '/book')
	data = r.json()

	return (float(data['bids'][0][0]), exchange_symbol, region_symbol)

def _guess_price():
	guess_dollar = random.randint(0,20000)
	guess_cents = random.randint(0,100)

	return float(guess_dollar) + (float(guess_cents) / 100.00)

def __main__():

	# seed a guess
	random.seed(int(time.time() * 100))
	
	# guess a price
	guess = _guess_price()

	# get price as well as exchange_symbol and region_symbol for given currency and region
	price, exchange_symbol, region_symbol = _get_price()

	print("The current exchange of %s is%s: %s%.2f" % \
		(exchange_symbol, "" if guess == price else " not", region_symbol, guess))

if __name__ == '__main__':
	__main__()
