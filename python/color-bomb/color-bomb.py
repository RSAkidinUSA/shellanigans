#!/usr/bin/python3
import random
import time
import subprocess

# Colors
COLORS = {'red' : 31, 'green' : 32, 'norm' : 0}

def print_func(sub):
	while ( True ):
		print("\x1b[" + str(COLORS[random.choice(list(COLORS.keys()))]) + "m", end='', flush=True)
		for i in range(random.randint(1,10)):
			if (sub.poll() != None):
				return
			time.sleep(0.2)


def main():
	# setup to launch in background
	args = '/bin/bash'
	# setup random delay
	random.seed(time.time())
	# Open a new shell
	sub = subprocess.Popen(args)
	# Run function in background
	print_func(sub)
	print("\x1b[0mThanks for playing ;)", flush=True)

if __name__ == '__main__':
	main()