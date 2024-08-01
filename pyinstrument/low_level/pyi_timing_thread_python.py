import threading
import time

current_time = 0.0

subscriber_lock = threading.Lock()
update_lock = threading.Lock()
thread_should_exit = False
thread_alive = False


class Subscription:
    def __init__(self, interval: float, id: int):
        self.interval = interval
        self.id = id


subscribers = []


def get_interval(max_interval: float):
    if subscribers:
        return min(sub.interval for sub in subscribers)
    return max_interval


def timing_thread():
    global current_time, thread_should_exit

    while not thread_should_exit:
        interval = get_interval(1.0)
        acquired = update_lock.acquire(timeout=interval)
        if acquired:
            update_lock.release()
        current_time = time.perf_counter()


def pyi_timing_thread_subscribe(desired_interval: float):
    global thread_alive, thread_should_exit, current_time

    with subscriber_lock:
        if not thread_alive:
            update_lock.acquire()
            thread_should_exit = False
            threading.Thread(target=timing_thread).start()
            thread_alive = True
            current_time = time.perf_counter()

        ids = [sub.id for sub in subscribers]
        new_id = 0
        while new_id in ids:
            new_id += 1

        subscribers.append(Subscription(desired_interval, new_id))

        update_lock.release()
        update_lock.acquire()

    return new_id


def pyi_timing_thread_unsubscribe(id: int):
    with subscriber_lock:
        subscriber_to_remove = next((sub for sub in subscribers if sub.id == id), None)

        if subscriber_to_remove:
            subscribers.remove(subscriber_to_remove)

            if not subscribers:
                global thread_should_exit, thread_alive
                thread_should_exit = True
                update_lock.release()
                thread_alive = False
            return 0
        else:
            raise Exception("PYI_TIMING_THREAD_NOT_SUBSCRIBED")


def pyi_timing_thread_get_time() -> float:
    return current_time


def pyi_timing_thread_get_interval() -> float:
    return get_interval(float("inf")) if thread_alive else -1.0
