#!/usr/bin/python3
import requests, random, time
API_URL = "https://api.gdax.com"

def __main__():
	currency = 'BTC-USD'
	currency_symbol = '$'
	r = requests.get(API_URL + '/products/' + currency + '/book')
	data = r.json()
	price = float(data['bids'][0][0])
	# probably should seed this better
	random.seed(int(time.time() * 100))
	guess_dollar = random.randint(0,20000)
	guess_cents = random.randint(0,100)

	guess = float(guess_dollar) + (float(guess_cents) / 100.00)

	print("The current price of %s is%s: %s%.2f" % \
		(currency, "" if guess == price else " not", currency_symbol, guess))

if __name__ == '__main__':
	__main__()
