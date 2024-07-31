#include "pyi_timing_thread.h"

#include <Python.h>
#include <time.h>
#include <float.h>

#include "pyi_floatclock.h"

static volatile double current_time = 0.0;

static PyThread_type_lock subscriber_lock = NULL;
static PyThread_type_lock update_lock = NULL;
static int thread_should_exit = 0;
static int thread_alive = 0;

// Structure to hold subscriptions
typedef struct Subscription {
    double interval;
    int id;
} Subscription;

#define MAX_SUBSCRIBERS 1000
static Subscription subscribers[MAX_SUBSCRIBERS];
static int subscriber_count = 0;

static double get_interval(double max_interval) {
    double min_interval = max_interval;

    for (int i = 0; i < subscriber_count; i++) {
        if (subscribers[i].interval < min_interval) {
            min_interval = subscribers[i].interval;
        }
    }

    return min_interval;
}

static void timing_thread(void* args) {
    while (!thread_should_exit) {
        double interval = get_interval(1.0);
        // sleep for the interval, or until we're woken up by a change
        PyLockStatus status = PyThread_acquire_lock_timed(
            update_lock,
            (PY_TIMEOUT_T)(interval * 1e6),
            0
        );
        if (status == PY_LOCK_ACQUIRED) {
            // rather than finishing the wait, another thread signaled a
            // change by releasing the lock. The lock was just for the sake of
            // the wakeup, so let's release it again.
            PyThread_release_lock(update_lock);
        }
        current_time = pyi_floatclock(PYI_FLOATCLOCK_DEFAULT);
    }
}

int pyi_timing_thread_subscribe(double desiredInterval) {
    if (subscriber_lock == NULL) {
        subscriber_lock = PyThread_allocate_lock();
    }
    if (update_lock == NULL) {
        update_lock = PyThread_allocate_lock();
    }

    PyThread_acquire_lock(subscriber_lock, WAIT_LOCK);

    if (!thread_alive) {
        PyThread_acquire_lock(update_lock, WAIT_LOCK);  // Initially hold the lock
        thread_should_exit = 0;
        PyThread_start_new_thread(timing_thread, NULL);
        thread_alive = 1;

        // initialise the current_time in case it's read immediately
        current_time = pyi_floatclock(PYI_FLOATCLOCK_DEFAULT);
    }

    int new_id = 0;

    // find an unused ID
    for (; new_id < MAX_SUBSCRIBERS; new_id++) {
        int already_exists = 0;
        for (int i = 0; i < subscriber_count; i++) {
            if (subscribers[i].id == new_id) {
                already_exists = 1;
                break;
            }
        }
        if (!already_exists) {
            break;
        }
    }
    if (new_id == MAX_SUBSCRIBERS) {
        // Too many subscribers
        PyThread_release_lock(subscriber_lock);
        return PYI_TIMING_THREAD_TOO_MANY_SUBSCRIBERS;
    }

    int index = subscriber_count;
    subscribers[index].id = new_id;
    subscribers[index].interval = desiredInterval;
    subscriber_count++;

    // signal a possible change in the interval
    PyThread_release_lock(update_lock);
    PyThread_acquire_lock(update_lock, WAIT_LOCK);

    PyThread_release_lock(subscriber_lock);
    return new_id;
}

int pyi_timing_thread_unsubscribe(int id) {
    PyThread_acquire_lock(subscriber_lock, WAIT_LOCK);

    int removals = 0;

    for (int i = 0; i < subscriber_count; i++) {
        if (subscribers[i].id == id) {
            // Removal: overwrite this one with with the last element and decrement count.
            subscribers[i] = subscribers[subscriber_count-1];
            subscriber_count--;
            removals++;
            break;
        }
    }

    // if the last subscriber was removed, stop the thread
    if (subscriber_count == 0) {
        thread_should_exit = 1;
        PyThread_release_lock(update_lock);
        thread_alive = 0;
    }

    PyThread_release_lock(subscriber_lock);

    if (removals == 0) {
        return PYI_TIMING_THREAD_NOT_SUBSCRIBED;
    } else {
        return 0;
    }
}

double pyi_timing_thread_get_time(void) {
    return current_time;
}

double pyi_timing_thread_get_interval(void) {
    if (thread_alive) {
        return get_interval(DBL_MAX);
    } else {
        return -1.0;
    }
}
