#ifndef PYI_FLOATCLOCK_H
#define PYI_FLOATCLOCK_H

#include <Python.h>

typedef enum {
    PYI_FLOATCLOCK_DEFAULT = 0,
    PYI_FLOATCLOCK_MONOTONIC_COARSE = 1,
} PYIFloatClockType;

PyAPI_FUNC(double) pyi_monotonic_coarse_resolution(void);
PyAPI_FUNC(double) pyi_floatclock(PYIFloatClockType timer);

#endif
