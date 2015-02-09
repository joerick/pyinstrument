#include <Python.h>
#include <structmember.h>

/*
These timer functions are mostly stolen from timemodule.c
*/

#if defined(MS_WINDOWS) && !defined(__BORLANDC__)
#include <windows.h>

/* use QueryPerformanceCounter on Windows */

static double
floatclock(void)
{
    static LARGE_INTEGER ctrStart;
    static double divisor = 0.0;
    LARGE_INTEGER now;
    double diff;

    if (divisor == 0.0) {
        LARGE_INTEGER freq;
        QueryPerformanceCounter(&ctrStart);
        if (!QueryPerformanceFrequency(&freq) || freq.QuadPart == 0) {
            /* Unlikely to happen - this works on all intel
               machines at least!  Revert to clock() */
            return PyFloat_FromDouble(((double)clock()) /
                                      CLOCKS_PER_SEC);
        }
        divisor = (double)freq.QuadPart;
    }
    QueryPerformanceCounter(&now);
    diff = (double)(now.QuadPart - ctrStart.QuadPart);
    return diff / divisor;
}

#else /* Not Windows */

#include <sys/time.h>

/* use gettimeofday */

static double
floatclock(void)
{
    struct timeval t;
    gettimeofday(&t, (struct timezone *)NULL);

    return (double)t.tv_sec + t.tv_usec*0.000001;
}

#endif

typedef struct {
    PyObject_HEAD
    PyObject *target;
    double interval;
    double last_invocation;
} RateLimiter;


static void
RateLimiter_dealloc(RateLimiter* self)
{
    Py_XDECREF(self->target);
    self->ob_type->tp_free((PyObject*)self);
}

static int
RateLimiter_init(RateLimiter *self, PyObject *args, PyObject *kwds)
{
    PyObject *target=NULL, *tmp;

    static char *kwlist[] = {"target", "interval", NULL};

    if (! PyArg_ParseTupleAndKeywords(args, kwds, "|Od", kwlist, &target, &self->interval))
        return -1; 

    if (!target) {
        PyErr_SetString(PyExc_TypeError, "target must not be none");
        return -1;
    }

    if (!PyCallable_Check(target)) {
        PyErr_SetString(PyExc_TypeError, "target must be callable");
        return -1;
    }

    tmp = self->target;
    Py_INCREF(target);
    self->target = target;
    Py_XDECREF(tmp);

    return 0;
}


static PyMemberDef RateLimiter_members[] = {
    {"target", T_OBJECT_EX, offsetof(RateLimiter, target), 0,
     "target function"},
    {"interval", T_DOUBLE, offsetof(RateLimiter, interval), 0,
     "desired interval in seconds"},
    {"last_invocation", T_DOUBLE, offsetof(RateLimiter, last_invocation), 0,
     "the time on the clock when target was last called"},
    {NULL}  /* Sentinel */
};

static PyObject *
RateLimiter_call(RateLimiter* self, PyObject *args, PyObject *kwds)
{
    double now = floatclock();

    if (now > self->last_invocation + self->interval) {
        PyObject *result = PyEval_CallObjectWithKeywords(self->target, args, kwds);

        self->last_invocation = now;

        return result;
    } 

    Py_RETURN_NONE;
}

static PyMethodDef RateLimiter_methods[] = {
    {NULL}  /* Sentinel */
};

static PyTypeObject RateLimiterType = {
    PyObject_HEAD_INIT(NULL)
    0,                                      /* ob_size */
    "rate_limiter.RateLimiter",             /* tp_name */
    sizeof(RateLimiter),                    /* tp_basicsize */
    0,                                      /* tp_itemsize */
    (destructor)RateLimiter_dealloc,        /* tp_dealloc */
    0,                                      /* tp_print */
    0,                                      /* tp_getattr */
    0,                                      /* tp_setattr */
    0,                                      /* tp_compare */
    0,                                      /* tp_repr */
    0,                                      /* tp_as_number */
    0,                                      /* tp_as_sequence */
    0,                                      /* tp_as_mapping */
    0,                                      /* tp_hash  */
    (ternaryfunc)RateLimiter_call,          /* tp_call */
    0,                                      /* tp_str */
    0,                                      /* tp_getattro */
    0,                                      /* tp_setattro */
    0,                                      /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                     /* tp_flags */
    "RateLimiter objects",                  /* tp_doc */
    0,                                      /* tp_traverse */
    0,                                      /* tp_clear */
    0,                                      /* tp_richcompare */
    0,                                      /* tp_weaklistoffset */
    0,                                      /* tp_iter */
    0,                                      /* tp_iternext */
    RateLimiter_methods,                    /* tp_methods */
    RateLimiter_members,                    /* tp_members */
    0,                                      /* tp_getset */
    0,                                      /* tp_base */
    0,                                      /* tp_dict */
    0,                                      /* tp_descr_get */
    0,                                      /* tp_descr_set */
    0,                                      /* tp_dictoffset */
    (initproc)RateLimiter_init,             /* tp_init */
    0,                                      /* tp_alloc */
    0,                                      /* tp_new */

};

static PyMethodDef rate_limiter_methods[] = {
    {NULL}  /* Sentinel */
};

#ifndef PyMODINIT_FUNC  /* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC
initrate_limiter(void) 
{
    PyObject* m;

    RateLimiterType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&RateLimiterType) < 0)
        return;

    m = Py_InitModule3("rate_limiter", rate_limiter_methods,
                       "Example module that creates an extension type.");

    Py_INCREF(&RateLimiterType);
    PyModule_AddObject(m, "RateLimiter", (PyObject *)&RateLimiterType);
}