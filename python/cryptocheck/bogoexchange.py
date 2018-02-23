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

def _get_cent_diff(a, b):
	tmp = str('%.2f' % (a - int(a),))
	tmp = tmp[2:]
	return int(tmp)

def _guess_price(minPrice=0, maxPrice=20000.00):
	# guess a dollar range within the given range
	guess_dollar = random.randint(int(minPrice),int(maxPrice))

	# if same dollar amount, set the max cent value at the max
	maxCents = _get_cent_diff(maxPrice, int(maxPrice)) if guess_dollar == int(maxPrice) else 100
	# if same dollar amount, set the min cent value at the min
	minCents = _get_cent_diff(minPrice, int(minPrice)) if guess_dollar == int(minPrice) else 0
	
	guess_cents = random.randint(minCents, maxCents)

	return float(guess_dollar) + (float(guess_cents) / 100.00)

def _parse_args():
	parser = argparse.ArgumentParser(description='Determine crypto currency exchange rate '\
									'following a bogosort approach!')
	parser.add_argument('-c', '--crypto', choices=crypto_list, default='BTC',
	                    help='Crypto currency to be exchanged')
	parser.add_argument('-r', '--region', choices=region_dict.keys(), default='US',
	                    help='Region of exchange')
	parser.add_argument('--guess-again', action='store_true', dest='guess_again',
						help='Keep running until the correct price is guessed')

	return parser.parse_args()

def __main__():

	args = _parse_args()

	# seed a guess
	random.seed(int(time.time() * 100))

	# get price as well as exchange_symbol and region_symbol for given currency and region
	price, exchange_symbol, region_symbol = _get_price(region=args.region, crypto=args.crypto)
	numGuesses = 0
	minPrice = 0
	maxPrice = 20000.00

	while (args.guess_again or numGuesses == 0):

		# guess a price
		guess = _guess_price(minPrice, maxPrice)
		numGuesses = numGuesses + 1
		
		if (price != None and price > minPrice and price < maxPrice):
			found = (str('%.2f' % (guess,)) == str('%.2f' % (price,)))
			print("The current exchange of %s is%s: %s%.2f" % \
				(exchange_symbol, "" if found else " not", region_symbol, guess))
			if (found):
				print("This program took %d guesses to determine the exchange rate!" % (numGuesses,))
				break				
			elif (guess < price):
				minPrice = guess
			else:
				maxPrice = guess
		elif (price == None):
			print("That combination is not currently available for comparison")
			break
		else:
			print("Sorry, %s is not within the provided price range" % (exchange_symbol,))
			break

if __name__ == '__main__':
	__main__()
