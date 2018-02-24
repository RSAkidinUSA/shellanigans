# python
This directory contains various python scripts to make your life easier

Makefile:

- Use "make install-(script)" to install a specific script
- Use "make install" to install all scripts
- Check the script section in this readme to see more about the script

cryptocheck.py:
Checks the current price of bitcoin for you, using a similar strategy to that of [bogosort](https://en.wikipedia.org/wiki/Bogosort)

```
usage: bogoexchange.py [-h] [-c {BTC,LTC,ETH,BCH}] [-r {EU,US,UK}]
                       [--guess-again] [-b]

Determine crypto currency exchange rate following a bogosort approach!

optional arguments:
  -h, --help            show this help message and exit
  -c {BTC,LTC,ETH,BCH}, --crypto {BTC,LTC,ETH,BCH}
                        Crypto currency to be exchanged
  -r {EU,US,UK}, --region {EU,US,UK}
                        Region of exchange
  --guess-again         Keep running until the correct price is guessed
  -b                    Bound the bogo algorithm: -b: minor bounding, -bb:
                        major bounding (Warning, this will reduce the bogoness
                        of this program... you don't want to do that, do you?
```	
