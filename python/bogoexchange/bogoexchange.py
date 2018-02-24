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

'''
# Class for bounding argument of argparse
class BAction(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        # print 'values: {v!r}'.format(v=values)
        if values==None:
            values='1'
        try:
            values=int(values)
        except ValueError:
            values=values.count('b')+1
        setattr(args, self.dest, values)
'''

def _parse_args():
	parser = argparse.ArgumentParser(description='Determine crypto currency exchange rate '\
									'following a bogosort approach!')
	parser.add_argument('-c', '--crypto', choices=crypto_list, default='BTC',
	                    help='Crypto currency to be exchanged')
	parser.add_argument('-r', '--region', choices=region_dict.keys(), default='US',
	                    help='Region of exchange')
	parser.add_argument('--guess-again', action='store_true', dest='guess_again',
						help='Keep running until the correct price is guessed')
	parser.add_argument('-b', action='count', dest='bound',
						help='Bound the bogo algorithm: -b: minor bounding, -bb: major bounding '\
						'(Warning, this will reduce the bogoness of this program... you don\'t '\
						'want to do that, do you?')

	return parser.parse_args()


# Used for maintaining price range and adjusting it accordingly
class priceCheck:
	__minPrice = 0.00
	__maxPrice = 20000.00
	__boundingLevel = 0
	__price = 0.00
	# upper and lower bound increments for -b
	__upperBoundDec = 0
	__lowerBoundInc = 0
	
	# Set the range of allowable guesses
	def __init__(self, minPrice=0.00, maxPrice=20000.00, bound=0, actual=0.00):
		self.__minPrice=minPrice
		self.__maxPrice=maxPrice
		self.__upperBoundDec=int((maxPrice-actual)/10)
		self.__lowerBoundInc=int((actual-minPrice)/10)
		self.__bound=bound
		self.__price=actual

	# Update the range after a guess
	def _update(self, guess):
		if (self.__boundingLevel == 1):
			# Do something
			self.__minPrice = self.__minPrice + self.__lowerBoundInc
			self.__maxPrice = self.__maxPrice - self.__upperBoundDec
		elif (self.__bound == 2):
			if (guess < self.__price):
				self.__minPrice = guess
			else:
				self.__maxPrice = guess

	# Check if a given price less than greater than or equal
	# Return 1 if greater, 0 if equal, -1 if less
	def check(self, guess):
		ret = (str('%.2f' % (guess,)) == str('%.2f' % (self.__price,)))
		if (ret):
			return 0
		elif (guess < self.__price):
			ret = -1
		else:
			ret = 1
		self._update(guess)
		return ret

	# Check if the given price is in the range
	# return True if valid, False if not
	def valid(self):
		return True if (self.__price < self.__maxPrice and \
						self.__price > self.__minPrice) else False

	# Generate a guess for the price of the exchange
	def guess_price(self):
		# guess a dollar range within the given range
		guess_dollar = random.randint(int(self.__minPrice),int(self.__maxPrice))

		# if same dollar amount, set the max cent value at the max
		maxCents = self._get_cent_diff('max') if guess_dollar == int(self.__maxPrice) else 100
		# if same dollar amount, set the min cent value at the min
		minCents = self._get_cent_diff('min') if guess_dollar == int(self.__minPrice) else 0
		
		guess_cents = random.randint(minCents, maxCents)

		return float(guess_dollar) + (float(guess_cents) / 100.00)

	# Get the difference in cents between two floats
	def _get_cent_diff(self, val='max'):
		if (val == 'max'):
			a = self.__maxPrice
		else:
			a = self.__minPrice

		tmp = str('%.2f' % (a - int(a),))
		tmp = tmp[2:]
		return int(tmp)

	# Print the current range (Debuggin purposes)
	def __repr__(self):
		return "<PriceRange: %.2f - %.2f>" % (self.__minPrice, self.__maxPrice)


# main, you know, the function that always runs!
def __main__():

	args = _parse_args()

	# seed a guess
	random.seed(int(time.time() * 100))

	# get price as well as exchange_symbol and region_symbol for given currency and region
	price, exchange_symbol, region_symbol = _get_price(region=args.region, crypto=args.crypto)
	if (price == None):
		print("That combination is not currently available for comparison")
		return

	PR = priceCheck(minPrice=0, maxPrice=20000.00, bound=args.bound, actual=price)
	numGuesses = 0

	while (args.guess_again or numGuesses == 0):

		# guess a price
		guess = PR.guess_price()
		numGuesses = numGuesses + 1
		
		if (PR.valid()):
			found = PR.check(guess)
			print("The current exchange of %s is%s: %s%.2f" % \
				(exchange_symbol, " not" if found else "", region_symbol, guess))
			if (found == 0):
				print("This program took %d guesses to determine the exchange rate!" % (numGuesses,))
				break
		else:
			print("Sorry, %s is not within the provided price range" % (exchange_symbol,))
			break

if __name__ == '__main__':
	__main__()
