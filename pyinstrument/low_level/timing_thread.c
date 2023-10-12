#include <Python.h>
#include <pythread.h>
#include <time.h>

typedef struct {
    PyObject_HEAD
    time_t current_time;
    long interval;
    int should_run;
    PyThread_type_lock lock;
    long thread_id;
} TimingThread;

void *update_time_thread(void *timing_thread_obj) {
    TimingThread *self = (TimingThread *)timing_thread_obj;

    while (self->should_run) {
        self->current_time = time(NULL);

        PyThread_acquire_lock(self->lock, 1);
        PyThread_release_lock(self->lock);

        PyThread_sleep(self->interval);
    }

    PyThread_exit_thread();
    return NULL;
}

static void TimingThread_dealloc(TimingThread* self) {
    if (self->should_run) {
        self->should_run = 0;
        PyThread_acquire_lock(self->lock, 1);
        PyThread_release_lock(self->lock);
    }

    if (self->lock) {
        PyThread_free_lock(self->lock);
    }

    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* TimingThread_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    TimingThread *self;

    self = (TimingThread *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->current_time = time(NULL);
        self->interval = 1;
        self->should_run = 1; // Start the thread by default on creation
        self->lock = PyThread_allocate_lock();
        self->thread_id = PyThread_start_new_thread(update_time_thread, (void *)self);
    }

    return (PyObject *)self;
}

static PyTypeObject TimingThreadType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "timingthread.TimingThread",
    .tp_doc = "TimingThread object that keeps track of time in a thread.",
    .tp_basicsize = sizeof(TimingThread),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = TimingThread_new,
    .tp_dealloc = (destructor)TimingThread_dealloc,
};

static struct PyModuleDef timingthreadmodule = {
    PyModuleDef_HEAD_INIT,
    .m_name = "timingthread",
    .m_doc = "Internal TimingThread object.",
    .m_size = -1,
};

PyMODINIT_FUNC PyInit_timingthread(void) {
    PyObject *m;

    if (PyType_Ready(&TimingThreadType) < 0)
        return NULL;

    m = PyModule_Create(&timingthreadmodule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&TimingThreadType);
    PyModule_AddObject(m, "TimingThread", (PyObject *)&TimingThreadType);

    return m;
}
