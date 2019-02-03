# this script just does a busywait for 0.25 seconds.
from __future__ import print_function
import time, sys

def do_nothing():
    pass

def busy_wait(duration):
    end_time = time.time() + duration

    while time.time() < end_time:
        do_nothing()

def main():
    print('sys.argv: ', sys.argv)
    busy_wait(0.25)


if __name__ == '__main__':
    main()
