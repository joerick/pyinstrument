#ifndef PYI_FLOATCLOCK_H
#define PYI_FLOATCLOCK_H

#include <Python.h>
#include "pyi_shared.h"

typedef enum {
    PYI_FLOATCLOCK_DEFAULT = 0,
    PYI_FLOATCLOCK_MONOTONIC_COARSE = 1,
} PYIFloatClockType;

Py_EXPORTED_SYMBOL double pyi_monotonic_coarse_resolution(void);
Py_EXPORTED_SYMBOL double pyi_floatclock(PYIFloatClockType timer);

#endif
