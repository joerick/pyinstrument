#ifndef PYI_TIMINGTHREAD_H
#define PYI_TIMINGTHREAD_H

#include <Python.h>
#include "pyi_shared.h"

/**
 * Adds a subscription to the timing thread, requesting that it updates the
 * time every `desired_interval` seconds. Returns an ID that can be used to
 * unsubscribe later, or a negative value indicating error.
 */

Py_EXPORTED_SYMBOL int pyi_timing_thread_subscribe(double desired_interval);

/**
 * Returns the current time, as updated by the timing thread.
 */
Py_EXPORTED_SYMBOL double pyi_timing_thread_get_time(void);

/**
 * Returns the current interval, or -1 if the thread is not running.
 */
Py_EXPORTED_SYMBOL double pyi_timing_thread_get_interval(void);

/**
 * Unsubscribes from the timing thread. Returns 0 on success, or a negative
 * value indicating error.
 */
Py_EXPORTED_SYMBOL int pyi_timing_thread_unsubscribe(int id);

#define PYI_TIMING_THREAD_UNKNOWN_ERROR -1
#define PYI_TIMING_THREAD_TOO_MANY_SUBSCRIBERS -2
#define PYI_TIMING_THREAD_NOT_SUBSCRIBED -3

#endif /* PYI_TIMINGTHREAD_H */
