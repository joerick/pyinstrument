import time


def D():
    time.sleep(0.7)


def C():
    __tracebackhide__ = True
    time.sleep(0.1)
    D()


def B():
    __tracebackhide__ = True
    time.sleep(0.1)
    C()


def A():
    time.sleep(0.1)
    B()


A()
