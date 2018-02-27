#!/usr/bin/python3
import random
import time
import subprocess
import psutil, os

# Colors
COLORS = {'red' : 31, 'green' : 32, 'norm' : 0}

# Python equivalent of which
# Stolen from https://gist.github.com/SEJeff/2576984
def which(exe=None):
    '''
    Python clone of POSIX's /usr/bin/which
    '''
    if exe:
        (path, name) = os.path.split(exe)
        if os.access(exe, os.X_OK):
            return exe
        for path in os.environ.get('PATH').split(os.pathsep):
            full_path = os.path.join(path, exe)
            if os.access(full_path, os.X_OK):
                return full_path
    return None

def print_func(sub):
	while ( True ):
		print("\x1b[" + str(COLORS[random.choice(list(COLORS.keys()))]) + "m", end='', flush=True)
		for i in range(random.randint(1,10)):
			if (sub.poll() != None):
				return
			time.sleep(0.2)


def main():
	# setup to launch in background
	parent = psutil.Process(psutil.Process(os.getpid()).ppid())
	args = which(parent.name())
	# Open a new shell
	sub = subprocess.Popen(args)
	# setup random delay
	random.seed(time.time())
	# Run function in background
	print_func(sub)
	print("\x1b[0mThanks for playing ;)", flush=True)

if __name__ == '__main__':
	main()