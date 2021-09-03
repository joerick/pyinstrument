#include <Python.h>
#include <structmember.h>
#include <frameobject.h>

////////////////////////////
// Version/Platform shims //
////////////////////////////

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
            return ((double)clock()) / CLOCKS_PER_SEC;
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

///////////////////
// ProfilerState //
///////////////////

typedef struct profiler_state {
    PyObject_HEAD
    PyObject *target;
    double interval;
    double last_invocation;
    PyObject *context_var;
    PyObject *last_context_var_value;
    PyObject *await_stack_list;
    PyObject *timer_func;
} ProfilerState;

static void ProfilerState_SetTarget(ProfilerState *self, PyObject *target) {
    PyObject *tmp = self->target;
    Py_XINCREF(target);
    self->target = target;
    Py_XDECREF(tmp);
}

/**
 * Updates last_context_var_value.
 *
 * Returns true on success, sets an exception and returns false on failure.
 * */
static int ProfilerState_UpdateContextVar(ProfilerState *self) {
    PyObject *old = self->last_context_var_value;
    PyObject *new = NULL;
    int status = PyContextVar_Get(self->context_var, NULL, &new);
    if (status == -1) {
        PyErr_SetString(PyExc_Exception, "failed to get value of the context var");
        return 0;
    }

    if (old == new) return 1;

    self->last_context_var_value = new;

    Py_XDECREF(old);

    return 1;
}

/**
 * Returns the current time for this profiler. On error, returns -1.0.
 */
static double ProfilerState_GetTime(ProfilerState *self) {
    if (self->timer_func != NULL) {
        // when a self->timer_func is set, call that.
#if PYTHON_VERSION_HEX >= 0x03090000
        PyObject *result = PyObject_CallNoArgs(self->timer_func);
#else
        PyObject *result = PyObject_CallObject(self->timer_func, NULL);
#endif
        if (result == NULL) {
            return -1.0;
        }

        if (!PyFloat_Check(result)) {
            PyErr_SetString(PyExc_RuntimeError, "custom time function must return a float");
            return -1.0;
        }

        double resultDouble = PyFloat_AsDouble(result);

        Py_DECREF(result);
        return resultDouble;
    } else {
        // otherwise as normal, call the C timer function.
        return floatclock();
    }
}

static void ProfilerState_Dealloc(ProfilerState *self) {
    ProfilerState_SetTarget(self, NULL);
    Py_XDECREF(self->context_var);
    Py_XDECREF(self->last_context_var_value);
    Py_XDECREF(self->await_stack_list);
    Py_XDECREF(self->timer_func);
    Py_TYPE(self)->tp_free(self);
}

static PyTypeObject ProfilerState_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "pyinstrument.stat_profile.ProfilerState",        /* tp_name */
    sizeof(ProfilerState),                    /* tp_basicsize */
    0,                                        /* tp_itemsize */
    (destructor)ProfilerState_Dealloc,        /* tp_dealloc */
    0,                                        /* tp_print */
    0,                                        /* tp_getattr */
    0,                                        /* tp_setattr */
    0,                                        /* tp_reserved */
    0,                                        /* tp_repr */
    0,                                        /* tp_as_number */
    0,                                        /* tp_as_sequence */
    0,                                        /* tp_as_mapping */
    0,                                        /* tp_hash */
    0,                                        /* tp_call */
    0,                                        /* tp_str */
    0,                                        /* tp_getattro */
    0,                                        /* tp_setattro */
    0,                                        /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    0,                                        /* tp_doc */
    0,                                        /* tp_traverse */
    0,                                        /* tp_clear */
    0,                                        /* tp_richcompare */
    0,                                        /* tp_weaklistoffset */
    0,                                        /* tp_iter */
    0,                                        /* tp_iternext */
    0,                                        /* tp_methods */
    0,                                        /* tp_members */
    0,                                        /* tp_getset */
    0,                                        /* tp_base */
    0,                                        /* tp_dict */
    0,                                        /* tp_descr_get */
    0,                                        /* tp_descr_set */
    0,                                        /* tp_dictoffset */
    0,                                        /* tp_init */
    PyType_GenericAlloc,                      /* tp_alloc */
    PyType_GenericNew,                        /* tp_new */
    PyObject_Del,                             /* tp_free */
};

static ProfilerState *ProfilerState_New(void) {
    ProfilerState *op = PyObject_New(ProfilerState, &ProfilerState_Type);
    op->target = NULL;
    op->interval = 0.0;
    op->last_invocation = 0.0;
    op->context_var = NULL;
    op->last_context_var_value = NULL;
    op->await_stack_list = PyList_New(0);
    op->timer_func = NULL;
    return op;
}

////////////////////////
// Internal functions //
////////////////////////

static PyObject *whatstrings[8] = {NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL};

#define WHAT_CALL 0
#define WHAT_EXCEPTION 1
#define WHAT_LINE 2
#define WHAT_RETURN 3
#define WHAT_C_CALL 4
#define WHAT_C_EXCEPTION 5
#define WHAT_C_RETURN 6
#define WHAT_CONTEXT_CHANGED 7

static int
trace_init(void)
{
    static char *whatnames[8] = {"call", "exception", "line", "return",
                                 "c_call", "c_exception", "c_return",
                                 "context_changed"};
    PyObject *name;
    int i;
    for (i = 0; i < 8; ++i) {
        if (whatstrings[i] == NULL) {
            name = PyUnicode_InternFromString(whatnames[i]);
            if (name == NULL)
                return -1;
            whatstrings[i] = name;
        }
    }
    return 0;
}

static PyObject *
call_target(ProfilerState *pState, PyFrameObject *frame, int what, PyObject *arg)
{
    PyFrame_FastToLocals(frame);

#if PYTHON_VERSION_HEX >= 0x03090000
    // vectorcall implemention could be faster, is available in Python 3.9
    PyObject *callargs[4] = { NULL, (PyObject *) frame, whatstrings[what], arg == NULL ? Py_None : arg };
    PyObject *result = PyObject_Vectorcall(pState->target, callargs + 1, 3 | PY_VECTORCALL_ARGUMENTS_OFFSET, NULL);
#else
    PyObject *result = PyObject_CallFunctionObjArgs(pState->target, (PyObject *) frame, whatstrings[what], arg == NULL ? Py_None : arg, NULL);
#endif

    PyFrame_LocalsToFast(frame, 1);

    if (result == NULL)
        PyTraceBack_Here(frame);

    return result;
}

//////////////////////
// Public functions //
//////////////////////

/**
 * The profile function. Passed to PyEval_SetProfile, and called with
 * function frames as the program executes by Python
 */
static int
profile(PyObject *op, PyFrameObject *frame, int what, PyObject *arg)
{
    ProfilerState *pState = (ProfilerState *)op;
    PyObject *result;

    double now = ProfilerState_GetTime(pState);
    if (now == -1.0) {
        PyEval_SetProfile(NULL, NULL);
        return -1;
    }

    // check for context var change, send context_changed event if seen
    if (pState->context_var) {
        PyObject *old_context_var_value = pState->last_context_var_value;
        Py_XINCREF(old_context_var_value);

        if (!ProfilerState_UpdateContextVar(pState)) {
            PyEval_SetProfile(NULL, NULL);
            return -1;
        }

        if (old_context_var_value != pState->last_context_var_value) {
            PyFrameObject *context_change_frame;
            if (what == WHAT_CALL && frame->f_back) {
                context_change_frame = frame->f_back;
            } else {
                context_change_frame = frame;
            }

            PyObject *context_change_arg = PyTuple_Pack(
                3,
                pState->last_context_var_value,
                old_context_var_value,
                pState->await_stack_list
            );

            result = call_target(pState, context_change_frame, WHAT_CONTEXT_CHANGED, context_change_arg);

            Py_DECREF(context_change_arg);

            if (result == NULL) {
                PyEval_SetProfile(NULL, NULL);
                return -1;
            }

            Py_DECREF(result);
        }

        Py_XDECREF(old_context_var_value);
    }

    // if we're returning from a coroutine, add that to the await stack
    if ((what == WHAT_RETURN) && (frame->f_code->co_flags & 0x80)) {
        PyObject *frame_identifier = PyUnicode_FromFormat(
            "%U%c%U%c%i",
            frame->f_code->co_name,
            0, // NULL char
            frame->f_code->co_filename,
            0, // NULL char
            frame->f_code->co_firstlineno
        );

        int status = PyList_Append(pState->await_stack_list, frame_identifier);
        Py_DECREF(frame_identifier);

        if (status == -1) {
            PyEval_SetProfile(NULL, NULL);
            return -1;
        }
    } else {
        // clear the list
        int status = PyList_SetSlice(
            pState->await_stack_list,
            0,
            PyList_GET_SIZE(pState->await_stack_list),
            NULL
        );

        if (status == -1) {
            PyEval_SetProfile(NULL, NULL);
            return -1;
        }
    }


    // stat profile
    if (now < pState->last_invocation + pState->interval) {
        return 0;
    }

    pState->last_invocation = now;
    result = call_target(pState, frame, what, arg);

    if (result == NULL) {
        PyEval_SetProfile(NULL, NULL);
        return -1;
    }

    Py_DECREF(result);
    return 0;
}

/**
 * The 'setprofile' function. This is the public API that can be called
 * from Python code.
 */
static PyObject *
setstatprofile(PyObject *m, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"target", "interval", "context_var", "timer_func", NULL};
    ProfilerState *pState = NULL;
    double interval = 0.0;
    PyObject *target = NULL;
    PyObject *context_var = NULL;
    PyObject *timer_func = NULL;

    if (! PyArg_ParseTupleAndKeywords(args, kwds, "O|dO!O", kwlist, &target, &interval, &PyContextVar_Type, &context_var, &timer_func))
        return NULL;

    if (target == Py_None) {
        target = NULL;
    }

    if (target) {
        if (!PyCallable_Check(target)) {
            PyErr_SetString(PyExc_TypeError, "target must be callable");
            return NULL;
        }

        if (trace_init() == -1)
            return NULL;

        pState = ProfilerState_New();
        ProfilerState_SetTarget(pState, target);

        // default interval is 1 ms
        pState->interval = (interval > 0) ? interval : 0.001;

        if (timer_func == Py_None) {
            timer_func = NULL;
        }

        if (timer_func) {
            Py_INCREF(timer_func);
            pState->timer_func = timer_func;
        }

        // initialise the last invocation to avoid immediate callback
        pState->last_invocation = ProfilerState_GetTime(pState);

        if (context_var) {
            Py_INCREF(context_var);
            pState->context_var = context_var;

            if (!ProfilerState_UpdateContextVar(pState)) {
                return NULL;
            }
        }

        PyEval_SetProfile(profile, (PyObject *)pState);
        Py_DECREF(pState);
    } else {
        PyEval_SetProfile(NULL, NULL);
    }

    Py_RETURN_NONE;
}

///////////////////////////
// Module initialization //
///////////////////////////

static PyMethodDef module_methods[] = {
    {"setstatprofile", (PyCFunction)setstatprofile, METH_VARARGS | METH_KEYWORDS,
     "Sets the statistal profiler callback. The function in the same manner as setprofile, but "
     "instead of being called every on every call and return, the function is called every "
     "<interval> seconds with the current stack."},
    {NULL}  /* Sentinel */
};

PyMODINIT_FUNC PyInit_stat_profile(void)
{
    PyType_Ready(&ProfilerState_Type);

    static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "stat_profile",
        "Module that implements the backend to a statistical profiler",
        -1,
        module_methods
    };

    return PyModule_Create(&moduledef);
}
