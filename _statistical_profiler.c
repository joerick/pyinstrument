#include <Python.h>
#include <structmember.h>
#include <frameobject.h>

/* Python 2 shim */
#if PY_MAJOR_VERSION < 3

#define PyUnicode_InternFromString PyString_InternFromString

#endif

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

#else  /* !MS_WINDOWS */

#include <sys/time.h>

static double
floatclock(void)
{
    struct timeval t;
    gettimeofday(&t, (struct timezone *)NULL);

    return (double)t.tv_sec + t.tv_usec*0.000001;
}

#endif  /* MS_WINDOWS */

static PyObject *whatstrings[7] = {NULL, NULL, NULL, NULL, NULL, NULL, NULL};

static int
trace_init(void)
{
    static char *whatnames[7] = {"call", "exception", "line", "return",
                                    "c_call", "c_exception", "c_return"};
    PyObject *name;
    int i;
    for (i = 0; i < 7; ++i) {
        if (whatstrings[i] == NULL) {
            name = PyUnicode_InternFromString(whatnames[i]);
            if (name == NULL)
                return -1;
            whatstrings[i] = name;
        }
    }
    return 0;
}

struct module_state {
    PyObject *target;
    double interval;
    double last_invocation;
};

#if PY_MAJOR_VERSION >= 3
#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))
#else
#define GETSTATE(m) (&_state)
static struct module_state _state;
#endif

static PyObject *
call_target(PyObject* m, PyFrameObject *frame, int what, PyObject *arg)
{
    struct module_state *mState = GETSTATE(m);

    PyObject *args;
    PyObject *whatstr;
    PyObject *result;

    if (arg == NULL)
        arg = Py_None;

    args = PyTuple_New(3);
    if (args == NULL)
        return NULL;

    PyFrame_FastToLocals(frame);

    Py_INCREF(frame);
    whatstr = whatstrings[what];
    Py_INCREF(whatstr);
    if (arg == NULL)
        arg = Py_None;
    Py_INCREF(arg);
    PyTuple_SET_ITEM(args, 0, (PyObject *)frame);
    PyTuple_SET_ITEM(args, 1, whatstr);
    PyTuple_SET_ITEM(args, 2, arg);

    /* call the Python-level target function */
    result = PyEval_CallObject(mState->target, args);

    PyFrame_LocalsToFast(frame, 1);
    if (result == NULL)
        PyTraceBack_Here(frame);

    /* cleanup */
    Py_DECREF(args);
    return result;
}

static int
profile(PyObject *m, PyFrameObject *frame, int what, PyObject *arg)
{
    double now = floatclock();
    struct module_state *mState = GETSTATE(m);

    if (now < mState->last_invocation + mState->interval) {
        return 0;
    } else {
        mState->last_invocation = now;
    }

    PyObject *result = call_target(m, frame, what, arg);

    if (result == NULL) {
        PyEval_SetProfile(NULL, NULL);
        return -1;
    }

    Py_DECREF(result);
    return 0;
}

static PyObject *
setstatprofile(PyObject *m, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"target", "interval", NULL};
    struct module_state *mState = GETSTATE(m);
    double interval = 0.0;
    PyObject *target = NULL;

    if (! PyArg_ParseTupleAndKeywords(args, kwds, "O|d", kwlist, &target, &interval))
        return NULL;

    if (target == Py_None) 
        target = NULL;

    if (target && !PyCallable_Check(target)) {
        PyErr_SetString(PyExc_TypeError, "target must be callable");
        return NULL;
    }

    PyObject *tmp = mState->target;
    Py_XINCREF(target);
    mState->target = target;
    Py_XDECREF(tmp);

    // default interval is 1 ms
    mState->interval = (interval > 0) ? interval : 0.001;

    if (target) {
        if (trace_init() == -1)
            return NULL;

        PyEval_SetProfile(profile, m);
    } else {
        PyEval_SetProfile(NULL, NULL);
    }

    Py_RETURN_NONE;
}

/*
    Module initialization
*/

#if PY_MAJOR_VERSION >= 3
    #define MOD_INIT(name) PyMODINIT_FUNC PyInit_##name(void)
    #define MOD_DEF(m, name, doc, methods, module_state_size) \
        static struct PyModuleDef moduledef = { \
            PyModuleDef_HEAD_INIT, name, doc, module_state_size, methods, }; \
        m = PyModule_Create(&moduledef);
    #define MOD_RETURN(m) return m;
#else
    #define MOD_INIT(name) PyMODINIT_FUNC init##name(void)
    #define MOD_DEF(m, name, doc, methods, module_state_size) \
        m = Py_InitModule3(name, methods, doc);
    #define MOD_RETURN(m) return;
#endif

static PyMethodDef module_methods[] = {
    {"setstatprofile", (PyCFunction)setstatprofile, METH_VARARGS | METH_KEYWORDS, 
     "Sets the statistal profiler callback. The function in the same manner as setprofile, but "
     "instead of being called every on every call and return, the function is called every "
     "<interval> seconds with the current stack."},
    {NULL}  /* Sentinel */
};

MOD_INIT(_statistical_profiler)
{
    PyObject* m;

    MOD_DEF(m, 
            "_statistical_profiler", 
            "Module that implements the frontend to a statistical profiler", 
            module_methods,
            sizeof(struct module_state))

    MOD_RETURN(m)
}
