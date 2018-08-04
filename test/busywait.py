# this script just does a busywait for 0.25 seconds.
import time

def do_nothing():
    pass

def busy_wait(duration):
    end_time = time.time() + duration

    while time.time() < end_time:
        do_nothing()

if __name__ == '__main__':
    busy_wait(0.25)
