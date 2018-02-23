#!/usr/bin/python3
#coding: <utf-8>

# A python script for (possibly) determining the current price of a crypto
# currency, following a similar approach to bogosort
import argparse
import requests
import random
import time
import sys

API_URL = "https://api.gdax.com"
crypto_list = ['BTC', 'LTC', 'ETH', 'BCH']
region_dict = { 'US' : {'symbol' : '$', 'string' : 'USD'}, \
				'UK' : {'symbol' : '£', 'string' : 'GBP'}, \
				'EU' : {'symbol' : '€', 'string' : 'EUR'} }

def _get_price(crypto='BTC', region='US'):
	# determine exchange symbol for currency and region
	exchange_symbol = crypto + '-' + region_dict[region]['string']
	region_symbol = region_dict[region]['symbol']
	
	r = requests.get(API_URL + '/products/' + exchange_symbol + '/book')
	data = r.json()
	try:
		retVal = (float(data['bids'][0][0]), exchange_symbol, region_symbol)
		return retVal
	except:
		return (None, exchange_symbol, region_symbol)


def _guess_price():
	guess_dollar = random.randint(0,20000)
	guess_cents = random.randint(0,100)

	return float(guess_dollar) + (float(guess_cents) / 100.00)

def _parse_args():
	parser = argparse.ArgumentParser(description='Determine crypto currency exchange rate '\
									'following a bogosort approach!')
	parser.add_argument('-c', '--crypto', choices=crypto_list, default='BTC',
	                    help='Crypto currency to be exchanged')
	parser.add_argument('-r', '--region', choices=region_dict.keys(), default='US',
	                    help='Region of exchange')

	return parser.parse_args()

def __main__():

	args = _parse_args()

	# seed a guess
	random.seed(int(time.time() * 100))
	
	# guess a price
	guess = _guess_price()

	# get price as well as exchange_symbol and region_symbol for given currency and region
	price, exchange_symbol, region_symbol = _get_price(region=args.region, crypto=args.crypto)

	if (price != None):
		print("The current exchange of %s is%s: %s%.2f" % \
			(exchange_symbol, "" if guess == price else " not", region_symbol, guess))
	else:
		print("That combination is not currently available for comparison")

if __name__ == '__main__':
	__main__()
