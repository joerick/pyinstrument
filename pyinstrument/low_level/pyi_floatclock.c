#include "pyi_floatclock.h"

#include <Python.h>
#include <time.h> // gettimeofday, clock()
#include <float.h> // DBL_MAX


/*
The windows implementations mostly stolen from timemodule.c
*/

#if defined(MS_WINDOWS) && !defined(__BORLANDC__)
#include <windows.h>

double pyi_monotonic_coarse_resolution(void)
{
    return DBL_MAX;
}

/* use QueryPerformanceCounter on Windows */

double pyi_floatclock(PYIFloatClockType timer)
{
    if (timer == PYI_FLOATCLOCK_MONOTONIC_COARSE) {
        warn_once("CLOCK_MONOTONIC_COARSE not available on this system.");
    }
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

#include <unistd.h>
#include <sys/time.h> // clock_gettime

static double SEC_PER_NSEC = 1e-9;
static double SEC_PER_USEC = 1e-6;

double pyi_monotonic_coarse_resolution(void)
{
#ifdef CLOCK_MONOTONIC_COARSE
    static double resolution = -1;
    if (resolution == -1) {
        struct timespec res;
        int success = clock_getres(CLOCK_MONOTONIC_COARSE, &res);
        if (success == 0) {
            resolution = res.tv_sec + res.tv_nsec * SEC_PER_NSEC;
        } else {
            // clock_getres failed, so let's set the resolution to something
            // so this timer is never used.
            resolution = DBL_MAX;
        }
    }
    return resolution;
#else
    return DBL_MAX;
#endif
}

double pyi_floatclock(PYIFloatClockType timer)
{
    // gets the current time in seconds, as quickly as possible.
#ifdef _POSIX_TIMERS
    struct timespec t;
    int res;
    if (timer == PYI_FLOATCLOCK_MONOTONIC_COARSE) {
# ifdef CLOCK_MONOTONIC_COARSE
        res = clock_gettime(CLOCK_MONOTONIC_COARSE, &t);
        if (res == 0) return t.tv_sec + t.tv_nsec * SEC_PER_NSEC;
# else
        warn_once("CLOCK_MONOTONIC_COARSE not available on this system.");
# endif
    }
# ifdef CLOCK_MONOTONIC
    res = clock_gettime(CLOCK_MONOTONIC, &t);
    if (res == 0) return t.tv_sec + t.tv_nsec * SEC_PER_NSEC;
# endif
    res = clock_gettime(CLOCK_REALTIME, &t);
    if (res == 0) return t.tv_sec + t.tv_nsec * SEC_PER_NSEC;
#endif
    struct timeval tv;
    gettimeofday(&tv, (struct timezone *)NULL);
    return (double)tv.tv_sec + tv.tv_usec * SEC_PER_USEC;
}

#endif  /* MS_WINDOWS */
