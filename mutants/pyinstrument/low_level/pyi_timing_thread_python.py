import threading
import time

current_time = 0.0

subscriber_lock = threading.Lock()
update_lock = threading.Lock()
thread_should_exit = False
thread_alive = False
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class Subscription:
    def xǁSubscriptionǁ__init____mutmut_orig(self, interval: float, id: int):
        self.interval = interval
        self.id = id
    def xǁSubscriptionǁ__init____mutmut_1(self, interval: float, id: int):
        self.interval = None
        self.id = id
    def xǁSubscriptionǁ__init____mutmut_2(self, interval: float, id: int):
        self.interval = interval
        self.id = None
    
    xǁSubscriptionǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSubscriptionǁ__init____mutmut_1': xǁSubscriptionǁ__init____mutmut_1, 
        'xǁSubscriptionǁ__init____mutmut_2': xǁSubscriptionǁ__init____mutmut_2
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSubscriptionǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁSubscriptionǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁSubscriptionǁ__init____mutmut_orig)
    xǁSubscriptionǁ__init____mutmut_orig.__name__ = 'xǁSubscriptionǁ__init__'


subscribers = []


def x_get_interval__mutmut_orig(max_interval: float):
    if subscribers:
        return min(sub.interval for sub in subscribers)
    return max_interval


def x_get_interval__mutmut_1(max_interval: float):
    if subscribers:
        return min(None)
    return max_interval

x_get_interval__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_interval__mutmut_1': x_get_interval__mutmut_1
}

def get_interval(*args, **kwargs):
    result = _mutmut_trampoline(x_get_interval__mutmut_orig, x_get_interval__mutmut_mutants, args, kwargs)
    return result 

get_interval.__signature__ = _mutmut_signature(x_get_interval__mutmut_orig)
x_get_interval__mutmut_orig.__name__ = 'x_get_interval'


def x_timing_thread__mutmut_orig():
    global current_time, thread_should_exit

    while not thread_should_exit:
        interval = get_interval(1.0)
        acquired = update_lock.acquire(timeout=interval)
        if acquired:
            update_lock.release()
        current_time = time.perf_counter()


def x_timing_thread__mutmut_1():
    global current_time, thread_should_exit

    while thread_should_exit:
        interval = get_interval(1.0)
        acquired = update_lock.acquire(timeout=interval)
        if acquired:
            update_lock.release()
        current_time = time.perf_counter()


def x_timing_thread__mutmut_2():
    global current_time, thread_should_exit

    while not thread_should_exit:
        interval = None
        acquired = update_lock.acquire(timeout=interval)
        if acquired:
            update_lock.release()
        current_time = time.perf_counter()


def x_timing_thread__mutmut_3():
    global current_time, thread_should_exit

    while not thread_should_exit:
        interval = get_interval(None)
        acquired = update_lock.acquire(timeout=interval)
        if acquired:
            update_lock.release()
        current_time = time.perf_counter()


def x_timing_thread__mutmut_4():
    global current_time, thread_should_exit

    while not thread_should_exit:
        interval = get_interval(2.0)
        acquired = update_lock.acquire(timeout=interval)
        if acquired:
            update_lock.release()
        current_time = time.perf_counter()


def x_timing_thread__mutmut_5():
    global current_time, thread_should_exit

    while not thread_should_exit:
        interval = get_interval(1.0)
        acquired = None
        if acquired:
            update_lock.release()
        current_time = time.perf_counter()


def x_timing_thread__mutmut_6():
    global current_time, thread_should_exit

    while not thread_should_exit:
        interval = get_interval(1.0)
        acquired = update_lock.acquire(timeout=None)
        if acquired:
            update_lock.release()
        current_time = time.perf_counter()


def x_timing_thread__mutmut_7():
    global current_time, thread_should_exit

    while not thread_should_exit:
        interval = get_interval(1.0)
        acquired = update_lock.acquire(timeout=interval)
        if acquired:
            update_lock.release()
        current_time = None

x_timing_thread__mutmut_mutants : ClassVar[MutantDict] = {
'x_timing_thread__mutmut_1': x_timing_thread__mutmut_1, 
    'x_timing_thread__mutmut_2': x_timing_thread__mutmut_2, 
    'x_timing_thread__mutmut_3': x_timing_thread__mutmut_3, 
    'x_timing_thread__mutmut_4': x_timing_thread__mutmut_4, 
    'x_timing_thread__mutmut_5': x_timing_thread__mutmut_5, 
    'x_timing_thread__mutmut_6': x_timing_thread__mutmut_6, 
    'x_timing_thread__mutmut_7': x_timing_thread__mutmut_7
}

def timing_thread(*args, **kwargs):
    result = _mutmut_trampoline(x_timing_thread__mutmut_orig, x_timing_thread__mutmut_mutants, args, kwargs)
    return result 

timing_thread.__signature__ = _mutmut_signature(x_timing_thread__mutmut_orig)
x_timing_thread__mutmut_orig.__name__ = 'x_timing_thread'


def x_pyi_timing_thread_subscribe__mutmut_orig(desired_interval: float):
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


def x_pyi_timing_thread_subscribe__mutmut_1(desired_interval: float):
    global thread_alive, thread_should_exit, current_time

    with subscriber_lock:
        if thread_alive:
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


def x_pyi_timing_thread_subscribe__mutmut_2(desired_interval: float):
    global thread_alive, thread_should_exit, current_time

    with subscriber_lock:
        if not thread_alive:
            update_lock.acquire()
            thread_should_exit = None
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


def x_pyi_timing_thread_subscribe__mutmut_3(desired_interval: float):
    global thread_alive, thread_should_exit, current_time

    with subscriber_lock:
        if not thread_alive:
            update_lock.acquire()
            thread_should_exit = True
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


def x_pyi_timing_thread_subscribe__mutmut_4(desired_interval: float):
    global thread_alive, thread_should_exit, current_time

    with subscriber_lock:
        if not thread_alive:
            update_lock.acquire()
            thread_should_exit = False
            threading.Thread(target=None).start()
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


def x_pyi_timing_thread_subscribe__mutmut_5(desired_interval: float):
    global thread_alive, thread_should_exit, current_time

    with subscriber_lock:
        if not thread_alive:
            update_lock.acquire()
            thread_should_exit = False
            threading.Thread(target=timing_thread).start()
            thread_alive = None
            current_time = time.perf_counter()

        ids = [sub.id for sub in subscribers]
        new_id = 0
        while new_id in ids:
            new_id += 1

        subscribers.append(Subscription(desired_interval, new_id))

        update_lock.release()
        update_lock.acquire()

    return new_id


def x_pyi_timing_thread_subscribe__mutmut_6(desired_interval: float):
    global thread_alive, thread_should_exit, current_time

    with subscriber_lock:
        if not thread_alive:
            update_lock.acquire()
            thread_should_exit = False
            threading.Thread(target=timing_thread).start()
            thread_alive = False
            current_time = time.perf_counter()

        ids = [sub.id for sub in subscribers]
        new_id = 0
        while new_id in ids:
            new_id += 1

        subscribers.append(Subscription(desired_interval, new_id))

        update_lock.release()
        update_lock.acquire()

    return new_id


def x_pyi_timing_thread_subscribe__mutmut_7(desired_interval: float):
    global thread_alive, thread_should_exit, current_time

    with subscriber_lock:
        if not thread_alive:
            update_lock.acquire()
            thread_should_exit = False
            threading.Thread(target=timing_thread).start()
            thread_alive = True
            current_time = None

        ids = [sub.id for sub in subscribers]
        new_id = 0
        while new_id in ids:
            new_id += 1

        subscribers.append(Subscription(desired_interval, new_id))

        update_lock.release()
        update_lock.acquire()

    return new_id


def x_pyi_timing_thread_subscribe__mutmut_8(desired_interval: float):
    global thread_alive, thread_should_exit, current_time

    with subscriber_lock:
        if not thread_alive:
            update_lock.acquire()
            thread_should_exit = False
            threading.Thread(target=timing_thread).start()
            thread_alive = True
            current_time = time.perf_counter()

        ids = None
        new_id = 0
        while new_id in ids:
            new_id += 1

        subscribers.append(Subscription(desired_interval, new_id))

        update_lock.release()
        update_lock.acquire()

    return new_id


def x_pyi_timing_thread_subscribe__mutmut_9(desired_interval: float):
    global thread_alive, thread_should_exit, current_time

    with subscriber_lock:
        if not thread_alive:
            update_lock.acquire()
            thread_should_exit = False
            threading.Thread(target=timing_thread).start()
            thread_alive = True
            current_time = time.perf_counter()

        ids = [sub.id for sub in subscribers]
        new_id = None
        while new_id in ids:
            new_id += 1

        subscribers.append(Subscription(desired_interval, new_id))

        update_lock.release()
        update_lock.acquire()

    return new_id


def x_pyi_timing_thread_subscribe__mutmut_10(desired_interval: float):
    global thread_alive, thread_should_exit, current_time

    with subscriber_lock:
        if not thread_alive:
            update_lock.acquire()
            thread_should_exit = False
            threading.Thread(target=timing_thread).start()
            thread_alive = True
            current_time = time.perf_counter()

        ids = [sub.id for sub in subscribers]
        new_id = 1
        while new_id in ids:
            new_id += 1

        subscribers.append(Subscription(desired_interval, new_id))

        update_lock.release()
        update_lock.acquire()

    return new_id


def x_pyi_timing_thread_subscribe__mutmut_11(desired_interval: float):
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
        while new_id not in ids:
            new_id += 1

        subscribers.append(Subscription(desired_interval, new_id))

        update_lock.release()
        update_lock.acquire()

    return new_id


def x_pyi_timing_thread_subscribe__mutmut_12(desired_interval: float):
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
            new_id = 1

        subscribers.append(Subscription(desired_interval, new_id))

        update_lock.release()
        update_lock.acquire()

    return new_id


def x_pyi_timing_thread_subscribe__mutmut_13(desired_interval: float):
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
            new_id -= 1

        subscribers.append(Subscription(desired_interval, new_id))

        update_lock.release()
        update_lock.acquire()

    return new_id


def x_pyi_timing_thread_subscribe__mutmut_14(desired_interval: float):
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
            new_id += 2

        subscribers.append(Subscription(desired_interval, new_id))

        update_lock.release()
        update_lock.acquire()

    return new_id


def x_pyi_timing_thread_subscribe__mutmut_15(desired_interval: float):
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

        subscribers.append(None)

        update_lock.release()
        update_lock.acquire()

    return new_id


def x_pyi_timing_thread_subscribe__mutmut_16(desired_interval: float):
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

        subscribers.append(Subscription(None, new_id))

        update_lock.release()
        update_lock.acquire()

    return new_id


def x_pyi_timing_thread_subscribe__mutmut_17(desired_interval: float):
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

        subscribers.append(Subscription(desired_interval, None))

        update_lock.release()
        update_lock.acquire()

    return new_id


def x_pyi_timing_thread_subscribe__mutmut_18(desired_interval: float):
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

        subscribers.append(Subscription(new_id))

        update_lock.release()
        update_lock.acquire()

    return new_id


def x_pyi_timing_thread_subscribe__mutmut_19(desired_interval: float):
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

        subscribers.append(Subscription(desired_interval, ))

        update_lock.release()
        update_lock.acquire()

    return new_id

x_pyi_timing_thread_subscribe__mutmut_mutants : ClassVar[MutantDict] = {
'x_pyi_timing_thread_subscribe__mutmut_1': x_pyi_timing_thread_subscribe__mutmut_1, 
    'x_pyi_timing_thread_subscribe__mutmut_2': x_pyi_timing_thread_subscribe__mutmut_2, 
    'x_pyi_timing_thread_subscribe__mutmut_3': x_pyi_timing_thread_subscribe__mutmut_3, 
    'x_pyi_timing_thread_subscribe__mutmut_4': x_pyi_timing_thread_subscribe__mutmut_4, 
    'x_pyi_timing_thread_subscribe__mutmut_5': x_pyi_timing_thread_subscribe__mutmut_5, 
    'x_pyi_timing_thread_subscribe__mutmut_6': x_pyi_timing_thread_subscribe__mutmut_6, 
    'x_pyi_timing_thread_subscribe__mutmut_7': x_pyi_timing_thread_subscribe__mutmut_7, 
    'x_pyi_timing_thread_subscribe__mutmut_8': x_pyi_timing_thread_subscribe__mutmut_8, 
    'x_pyi_timing_thread_subscribe__mutmut_9': x_pyi_timing_thread_subscribe__mutmut_9, 
    'x_pyi_timing_thread_subscribe__mutmut_10': x_pyi_timing_thread_subscribe__mutmut_10, 
    'x_pyi_timing_thread_subscribe__mutmut_11': x_pyi_timing_thread_subscribe__mutmut_11, 
    'x_pyi_timing_thread_subscribe__mutmut_12': x_pyi_timing_thread_subscribe__mutmut_12, 
    'x_pyi_timing_thread_subscribe__mutmut_13': x_pyi_timing_thread_subscribe__mutmut_13, 
    'x_pyi_timing_thread_subscribe__mutmut_14': x_pyi_timing_thread_subscribe__mutmut_14, 
    'x_pyi_timing_thread_subscribe__mutmut_15': x_pyi_timing_thread_subscribe__mutmut_15, 
    'x_pyi_timing_thread_subscribe__mutmut_16': x_pyi_timing_thread_subscribe__mutmut_16, 
    'x_pyi_timing_thread_subscribe__mutmut_17': x_pyi_timing_thread_subscribe__mutmut_17, 
    'x_pyi_timing_thread_subscribe__mutmut_18': x_pyi_timing_thread_subscribe__mutmut_18, 
    'x_pyi_timing_thread_subscribe__mutmut_19': x_pyi_timing_thread_subscribe__mutmut_19
}

def pyi_timing_thread_subscribe(*args, **kwargs):
    result = _mutmut_trampoline(x_pyi_timing_thread_subscribe__mutmut_orig, x_pyi_timing_thread_subscribe__mutmut_mutants, args, kwargs)
    return result 

pyi_timing_thread_subscribe.__signature__ = _mutmut_signature(x_pyi_timing_thread_subscribe__mutmut_orig)
x_pyi_timing_thread_subscribe__mutmut_orig.__name__ = 'x_pyi_timing_thread_subscribe'


def x_pyi_timing_thread_unsubscribe__mutmut_orig(id: int):
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


def x_pyi_timing_thread_unsubscribe__mutmut_1(id: int):
    with subscriber_lock:
        subscriber_to_remove = None

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


def x_pyi_timing_thread_unsubscribe__mutmut_2(id: int):
    with subscriber_lock:
        subscriber_to_remove = next(None, None)

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


def x_pyi_timing_thread_unsubscribe__mutmut_3(id: int):
    with subscriber_lock:
        subscriber_to_remove = next(None)

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


def x_pyi_timing_thread_unsubscribe__mutmut_4(id: int):
    with subscriber_lock:
        subscriber_to_remove = next((sub for sub in subscribers if sub.id == id), )

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


def x_pyi_timing_thread_unsubscribe__mutmut_5(id: int):
    with subscriber_lock:
        subscriber_to_remove = next((sub for sub in subscribers if sub.id != id), None)

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


def x_pyi_timing_thread_unsubscribe__mutmut_6(id: int):
    with subscriber_lock:
        subscriber_to_remove = next((sub for sub in subscribers if sub.id == id), None)

        if subscriber_to_remove:
            subscribers.remove(None)

            if not subscribers:
                global thread_should_exit, thread_alive
                thread_should_exit = True
                update_lock.release()
                thread_alive = False
            return 0
        else:
            raise Exception("PYI_TIMING_THREAD_NOT_SUBSCRIBED")


def x_pyi_timing_thread_unsubscribe__mutmut_7(id: int):
    with subscriber_lock:
        subscriber_to_remove = next((sub for sub in subscribers if sub.id == id), None)

        if subscriber_to_remove:
            subscribers.remove(subscriber_to_remove)

            if subscribers:
                global thread_should_exit, thread_alive
                thread_should_exit = True
                update_lock.release()
                thread_alive = False
            return 0
        else:
            raise Exception("PYI_TIMING_THREAD_NOT_SUBSCRIBED")


def x_pyi_timing_thread_unsubscribe__mutmut_8(id: int):
    with subscriber_lock:
        subscriber_to_remove = next((sub for sub in subscribers if sub.id == id), None)

        if subscriber_to_remove:
            subscribers.remove(subscriber_to_remove)

            if not subscribers:
                global thread_should_exit, thread_alive
                thread_should_exit = None
                update_lock.release()
                thread_alive = False
            return 0
        else:
            raise Exception("PYI_TIMING_THREAD_NOT_SUBSCRIBED")


def x_pyi_timing_thread_unsubscribe__mutmut_9(id: int):
    with subscriber_lock:
        subscriber_to_remove = next((sub for sub in subscribers if sub.id == id), None)

        if subscriber_to_remove:
            subscribers.remove(subscriber_to_remove)

            if not subscribers:
                global thread_should_exit, thread_alive
                thread_should_exit = False
                update_lock.release()
                thread_alive = False
            return 0
        else:
            raise Exception("PYI_TIMING_THREAD_NOT_SUBSCRIBED")


def x_pyi_timing_thread_unsubscribe__mutmut_10(id: int):
    with subscriber_lock:
        subscriber_to_remove = next((sub for sub in subscribers if sub.id == id), None)

        if subscriber_to_remove:
            subscribers.remove(subscriber_to_remove)

            if not subscribers:
                global thread_should_exit, thread_alive
                thread_should_exit = True
                update_lock.release()
                thread_alive = None
            return 0
        else:
            raise Exception("PYI_TIMING_THREAD_NOT_SUBSCRIBED")


def x_pyi_timing_thread_unsubscribe__mutmut_11(id: int):
    with subscriber_lock:
        subscriber_to_remove = next((sub for sub in subscribers if sub.id == id), None)

        if subscriber_to_remove:
            subscribers.remove(subscriber_to_remove)

            if not subscribers:
                global thread_should_exit, thread_alive
                thread_should_exit = True
                update_lock.release()
                thread_alive = True
            return 0
        else:
            raise Exception("PYI_TIMING_THREAD_NOT_SUBSCRIBED")


def x_pyi_timing_thread_unsubscribe__mutmut_12(id: int):
    with subscriber_lock:
        subscriber_to_remove = next((sub for sub in subscribers if sub.id == id), None)

        if subscriber_to_remove:
            subscribers.remove(subscriber_to_remove)

            if not subscribers:
                global thread_should_exit, thread_alive
                thread_should_exit = True
                update_lock.release()
                thread_alive = False
            return 1
        else:
            raise Exception("PYI_TIMING_THREAD_NOT_SUBSCRIBED")


def x_pyi_timing_thread_unsubscribe__mutmut_13(id: int):
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
            raise Exception(None)


def x_pyi_timing_thread_unsubscribe__mutmut_14(id: int):
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
            raise Exception("XXPYI_TIMING_THREAD_NOT_SUBSCRIBEDXX")


def x_pyi_timing_thread_unsubscribe__mutmut_15(id: int):
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
            raise Exception("pyi_timing_thread_not_subscribed")

x_pyi_timing_thread_unsubscribe__mutmut_mutants : ClassVar[MutantDict] = {
'x_pyi_timing_thread_unsubscribe__mutmut_1': x_pyi_timing_thread_unsubscribe__mutmut_1, 
    'x_pyi_timing_thread_unsubscribe__mutmut_2': x_pyi_timing_thread_unsubscribe__mutmut_2, 
    'x_pyi_timing_thread_unsubscribe__mutmut_3': x_pyi_timing_thread_unsubscribe__mutmut_3, 
    'x_pyi_timing_thread_unsubscribe__mutmut_4': x_pyi_timing_thread_unsubscribe__mutmut_4, 
    'x_pyi_timing_thread_unsubscribe__mutmut_5': x_pyi_timing_thread_unsubscribe__mutmut_5, 
    'x_pyi_timing_thread_unsubscribe__mutmut_6': x_pyi_timing_thread_unsubscribe__mutmut_6, 
    'x_pyi_timing_thread_unsubscribe__mutmut_7': x_pyi_timing_thread_unsubscribe__mutmut_7, 
    'x_pyi_timing_thread_unsubscribe__mutmut_8': x_pyi_timing_thread_unsubscribe__mutmut_8, 
    'x_pyi_timing_thread_unsubscribe__mutmut_9': x_pyi_timing_thread_unsubscribe__mutmut_9, 
    'x_pyi_timing_thread_unsubscribe__mutmut_10': x_pyi_timing_thread_unsubscribe__mutmut_10, 
    'x_pyi_timing_thread_unsubscribe__mutmut_11': x_pyi_timing_thread_unsubscribe__mutmut_11, 
    'x_pyi_timing_thread_unsubscribe__mutmut_12': x_pyi_timing_thread_unsubscribe__mutmut_12, 
    'x_pyi_timing_thread_unsubscribe__mutmut_13': x_pyi_timing_thread_unsubscribe__mutmut_13, 
    'x_pyi_timing_thread_unsubscribe__mutmut_14': x_pyi_timing_thread_unsubscribe__mutmut_14, 
    'x_pyi_timing_thread_unsubscribe__mutmut_15': x_pyi_timing_thread_unsubscribe__mutmut_15
}

def pyi_timing_thread_unsubscribe(*args, **kwargs):
    result = _mutmut_trampoline(x_pyi_timing_thread_unsubscribe__mutmut_orig, x_pyi_timing_thread_unsubscribe__mutmut_mutants, args, kwargs)
    return result 

pyi_timing_thread_unsubscribe.__signature__ = _mutmut_signature(x_pyi_timing_thread_unsubscribe__mutmut_orig)
x_pyi_timing_thread_unsubscribe__mutmut_orig.__name__ = 'x_pyi_timing_thread_unsubscribe'


def pyi_timing_thread_get_time() -> float:
    return current_time


def x_pyi_timing_thread_get_interval__mutmut_orig() -> float:
    return get_interval(float("inf")) if thread_alive else -1.0


def x_pyi_timing_thread_get_interval__mutmut_1() -> float:
    return get_interval(None) if thread_alive else -1.0


def x_pyi_timing_thread_get_interval__mutmut_2() -> float:
    return get_interval(float(None)) if thread_alive else -1.0


def x_pyi_timing_thread_get_interval__mutmut_3() -> float:
    return get_interval(float("XXinfXX")) if thread_alive else -1.0


def x_pyi_timing_thread_get_interval__mutmut_4() -> float:
    return get_interval(float("INF")) if thread_alive else -1.0


def x_pyi_timing_thread_get_interval__mutmut_5() -> float:
    return get_interval(float("inf")) if thread_alive else +1.0


def x_pyi_timing_thread_get_interval__mutmut_6() -> float:
    return get_interval(float("inf")) if thread_alive else -2.0

x_pyi_timing_thread_get_interval__mutmut_mutants : ClassVar[MutantDict] = {
'x_pyi_timing_thread_get_interval__mutmut_1': x_pyi_timing_thread_get_interval__mutmut_1, 
    'x_pyi_timing_thread_get_interval__mutmut_2': x_pyi_timing_thread_get_interval__mutmut_2, 
    'x_pyi_timing_thread_get_interval__mutmut_3': x_pyi_timing_thread_get_interval__mutmut_3, 
    'x_pyi_timing_thread_get_interval__mutmut_4': x_pyi_timing_thread_get_interval__mutmut_4, 
    'x_pyi_timing_thread_get_interval__mutmut_5': x_pyi_timing_thread_get_interval__mutmut_5, 
    'x_pyi_timing_thread_get_interval__mutmut_6': x_pyi_timing_thread_get_interval__mutmut_6
}

def pyi_timing_thread_get_interval(*args, **kwargs):
    result = _mutmut_trampoline(x_pyi_timing_thread_get_interval__mutmut_orig, x_pyi_timing_thread_get_interval__mutmut_mutants, args, kwargs)
    return result 

pyi_timing_thread_get_interval.__signature__ = _mutmut_signature(x_pyi_timing_thread_get_interval__mutmut_orig)
x_pyi_timing_thread_get_interval__mutmut_orig.__name__ = 'x_pyi_timing_thread_get_interval'
