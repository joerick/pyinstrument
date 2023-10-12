/* TimingThread.h */
#ifndef TIMINGTHREAD_H
#define TIMINGTHREAD_H

#include <Python.h>

typedef struct {
    PyObject_HEAD
    time_t current_time;
    long interval;
    int should_run;
    PyThread_type_lock lock;
    long thread_id;
} TimingThread;

PyMODINIT_FUNC PyInit_timingthread(void);

#endif /* TIMINGTHREAD_H */
