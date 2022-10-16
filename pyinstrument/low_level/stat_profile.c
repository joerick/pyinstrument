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

#if PY_VERSION_HEX >= 0x030b0000 // Python 3.11.0
#define PyFrame_GETBACK(f) PyFrame_GetBack(f)
#else
static PyFrameObject *
_PyFrame_GetBack(PyFrameObject *frame) {
    Py_XINCREF(frame->f_back);
    return frame->f_back;
}
#define PyFrame_GETBACK(f) _PyFrame_GetBack(f)
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
#if PY_VERSION_HEX >= 0x03090000
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

static PyObject *SELF_STRING = NULL;
static PyObject *CLS_STRING = NULL;
static PyObject *TRACEBACKHIDE_STRING = NULL;

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

    SELF_STRING = PyUnicode_InternFromString("self");
    if (SELF_STRING == NULL) return -1;

    CLS_STRING = PyUnicode_InternFromString("cls");
    if (CLS_STRING == NULL) return -1;

    TRACEBACKHIDE_STRING = PyUnicode_InternFromString("__tracebackhide__");
    if (TRACEBACKHIDE_STRING == NULL) return -1;

    return 0;
}

static PyObject *
call_target(ProfilerState *pState, PyFrameObject *frame, int what, PyObject *arg)
{
    PyFrame_FastToLocals(frame);

#if PY_VERSION_HEX >= 0x03090000
    // vectorcall implementation could be faster, is available in Python 3.9
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

static PyCodeObject *
code_from_frame(PyFrameObject* frame)
{
#if PY_VERSION_HEX >= 0x03090000
    return PyFrame_GetCode(frame);
#else
    PyCodeObject *result = frame->f_code;
    Py_XINCREF(result);
    return result;
#endif
}

static PyObject *
local_names_from_code(PyCodeObject *code)
{
#if PY_VERSION_HEX >= 0x030b0000
    return PyCode_GetVarnames(code);
#else
    PyObject *result = code->co_varnames;
    Py_XINCREF(result);
    return result;
#endif
}

#if PY_VERSION_HEX >= 0x030b0000 // Python 3.11.0
static const char *
_get_class_name_of_frame(PyFrameObject *frame, PyCodeObject *code) {
    PyObject *localsNames = PyCode_GetVarnames(code);

    if (localsNames == NULL) {
        return NULL;
    }

    PyObject *firstArgName = PyTuple_GET_ITEM(localsNames, 0);

    if (firstArgName == NULL) {
        return NULL;
    }


    int has_self = PyUnicode_Compare(firstArgName, SELF_STRING) == 0;
    int has_cls = PyUnicode_Compare(firstArgName, CLS_STRING) == 0;

    Py_DECREF(localsNames);

    if (!has_self && !has_cls) {
        // PyFrame_GetLocals is expensive and changes the frame, so we don't
        // want to call it unless we have to.
        return NULL;
    }

    const char *result = NULL;

    PyObject *locals = PyFrame_GetLocals(frame);

    if (!PyDict_Check(locals)) {
        Py_DECREF(locals);
        return NULL;
    }

    if (has_self) {
        PyObject *self = PyDict_GetItem(locals, SELF_STRING);
        if (self) {
            result = _PyType_Name(self->ob_type);
        }
    }
    else if (has_cls) {
        PyObject *cls = PyDict_GetItem(locals, CLS_STRING);
        if (cls) {
            if (PyType_Check(cls)) {
                PyTypeObject *type = (PyTypeObject *)cls;
                result = _PyType_Name(type);
            }
        }
    }

    Py_DECREF(locals);
    return result;
}

#else

static PyObject *
_get_first_arg_from_cell_variables(PyFrameObject *frame, PyCodeObject *code) {
    if (!code->co_cell2arg) {
        // we don't have args in cell variables
        return NULL;
    }

    Py_ssize_t ncells = PyTuple_GET_SIZE(code->co_cellvars);

    for (int i = 0; i < ncells; i++) {
        if (code->co_cell2arg[i] == CO_CELL_NOT_AN_ARG) {
            // this cell is not an argument
            continue;
        }

        // get the cell value
        // the cells are after the local variables
        PyObject *cell = frame->f_localsplus[code->co_nlocals + i];

        // return the value inside the cell
        if (!PyCell_Check(cell)) {
            continue;
        }

        return PyCell_GET(cell);
    }

    // cell variable not found
    return NULL;
}

static const char *
_get_class_name_of_frame(PyFrameObject *frame, PyCodeObject *code) {
    // This code looks only at the first 'fast' frame local.
    //
    // A generalisable way to get a local variable would be to look at every
    // local for one with the name 'self' or 'cls'. And such a general method
    // should also prefer f_locals, if it exists.
    //
    // But, function args are always be the first locals, self/cls is always
    // be the first arg, and f_localsplus is always set, even if f_locals
    // exists. So we only look at the first f_localsplus entry.

    if (code->co_argcount < 1) {
        return NULL;
    }

    if (!PyTuple_Check(code->co_varnames)) {
        // co_varnames must be a tuple
        return NULL;
    }

    if (code->co_nlocals < 1 || PyTuple_Size(code->co_varnames) < 1) {
        return NULL;
    }

    PyObject *first_var_name = PyTuple_GetItem(code->co_varnames, 0);
    int first_var_is_self = (PyUnicode_Compare(first_var_name, SELF_STRING) == 0);
    int first_var_is_cls = (PyUnicode_Compare(first_var_name, CLS_STRING) == 0);

    if (!(first_var_is_self || first_var_is_cls)) {
        return NULL;
    }

    PyObject *first_var = frame->f_localsplus[0];

    if (first_var == NULL) {
        // Sometimes arguments are in cells, if they're accessible from other
        // scopes, for example an inner function that captures self. In that
        // case, the local var is NULL, and it's stored as a cell instead.
        first_var = _get_first_arg_from_cell_variables(frame, code);
    }

    if (first_var == NULL) {
        // not sure why this would happen, but as a failsafe.
        return NULL;
    }

    if (first_var_is_self) {
        PyTypeObject *type = first_var->ob_type;
        return _PyType_Name(type);
    } else if (first_var_is_cls) {
        if (!PyType_Check(first_var)) {
            return NULL;
        }
        PyTypeObject *type = (PyTypeObject *)first_var;
        return _PyType_Name(type);
    } else {
        Py_FatalError("unreachable code");
    }

    return NULL;
}

#endif


/**
 * returns `1` if any variable named `"__trackbackhide__"` is defined in frame
 * locals, returns `0` otherwise
 */
static const int
_get_tracebackhide(PyFrameObject *frame, PyCodeObject *code) {
    PyObject *locals_names = local_names_from_code(code);

    if (locals_names == NULL) {
        return 0;
    }

    if (!PySequence_Check(locals_names)) {
        // locals_names must be a sequence
        return 0;
    }

    int tracebackhide = PySequence_Contains(locals_names, TRACEBACKHIDE_STRING);

    Py_DECREF(locals_names);

    if (tracebackhide < 0) {
        // in this case the PySequence_Contains function encountered an error
        Py_FatalError("could not determine names of frame local variables");
    } else {
        return tracebackhide;
    }
}

static PyObject *
_get_frame_info(PyFrameObject *frame) {
    PyCodeObject *code = code_from_frame(frame);

    PyObject *class_name_attribute;

    const char *class_name = _get_class_name_of_frame(frame, code);
    if (class_name == NULL) {
        class_name_attribute = PyUnicode_New(0, 127); // empty string
    } else {
        class_name_attribute = PyUnicode_FromFormat(
            "%c%c%s",
            1, // 0x01 char denotes 'attribute'
            'c', // 'c' char denotes 'class name'
            class_name
        );
    }

    PyObject *line_number_attribute;

    int line_number = PyFrame_GetLineNumber(frame);
    if (line_number < 1) {
        line_number_attribute = PyUnicode_New(0, 127);
    } else {
        line_number_attribute = PyUnicode_FromFormat(
            "%c%c%d",
            1,
            'l', // 'l' char denotes 'line number'
            line_number
        );
    }

    PyObject *frame_hidden_attribute;

    int tracebackhide = _get_tracebackhide(frame, code);
    if (tracebackhide <= 0) {
        frame_hidden_attribute = PyUnicode_New(0, 127);
    } else {
        frame_hidden_attribute = PyUnicode_FromFormat(
            "%c%c%c",
            1,
            'h', // 'h' char denotes 'frame hidden'
            '1' // '1' char denotes 'true'
        );
    }

    PyObject *result = PyUnicode_FromFormat(
        "%U%c%U%c%i%U%U%U",
        code->co_name,
        0, // NULL char
        code->co_filename,
        0, // NULL char
        code->co_firstlineno,
        class_name_attribute,
        line_number_attribute,
        frame_hidden_attribute
    );

    Py_DECREF(code);
    Py_DECREF(class_name_attribute);
    Py_DECREF(line_number_attribute);
    Py_DECREF(frame_hidden_attribute);

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
            PyFrameObject *context_change_frame; // borrowed reference
            PyFrameObject *parent_frame = PyFrame_GETBACK(frame); // strong reference, maybe null

            if (what == WHAT_CALL && parent_frame) {
                context_change_frame = parent_frame;
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
            Py_XDECREF(parent_frame);

            if (result == NULL) {
                PyEval_SetProfile(NULL, NULL);
                return -1;
            }

            Py_DECREF(result);
        }

        Py_XDECREF(old_context_var_value);
    }

    // if we're returning from a coroutine, add that to the await stack
    PyCodeObject* code = code_from_frame(frame);

    if ((what == WHAT_RETURN) && (code->co_flags & 0x80)) {
        PyObject *frame_identifier = _get_frame_info(frame);

        int status = PyList_Append(pState->await_stack_list, frame_identifier);
        Py_DECREF(frame_identifier);
        Py_DECREF(code);

        if (status == -1) {
            PyEval_SetProfile(NULL, NULL);
            return -1;
        }
    } else {
        Py_DECREF(code);

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


static PyObject *
get_frame_info(PyObject *m, PyObject *const *args, Py_ssize_t nargs)
{
    if (nargs != 1) {
        PyErr_SetString(PyExc_TypeError, "get_frame_info takes exactly 1 argument");
        return NULL;
    }

    if (!PyFrame_Check(args[0])) {
        PyErr_SetString(PyExc_TypeError, "get_frame_info should be called with a Frame object");
        return NULL;
    }

    PyFrameObject *frame = (PyFrameObject *)args[0];

    return _get_frame_info(frame);
}


///////////////////////////
// Module initialization //
///////////////////////////

static PyMethodDef module_methods[] = {
    {"setstatprofile", (PyCFunction)setstatprofile, METH_VARARGS | METH_KEYWORDS,
     "Sets the statistical profiler callback. The function in the same manner as setprofile, but "
     "instead of being called every on every call and return, the function is called every "
     "<interval> seconds with the current stack."},
    {"get_frame_info", (PyCFunction)get_frame_info, METH_FASTCALL,
     "Returns the frame identifier string for the given Frame object."},
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

    if (trace_init() == -1)
        return NULL;

    return PyModule_Create(&moduledef);
}
