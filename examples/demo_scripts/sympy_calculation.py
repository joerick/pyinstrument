# All right, here is a reproducer (sympy 1.12, pyinstrument 4.5.3, Python 3.11.5).
# With python sympy_instrument.py, prints This took 0:00:00.636278
# With pyinstrument sympy_instrument.py, prints This took 0:00:12.355938

from datetime import datetime

from sympy import FF, Poly, Rational, symbols, sympify  # type: ignore


def do_thing():
    # Some elliptic curve crypto stuff that is not important
    field = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
    params = {
        "a": 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC,
        "b": 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B,
    }
    k = FF(field)
    expr = sympify(f"3*b - b3", evaluate=False)
    for curve_param, value in params.items():
        expr = expr.subs(curve_param, k(value))
    param = str(expr.free_symbols.pop())

    def resolve(expression, k):
        if not expression.args:
            return expression
        args = []
        for arg in expression.args:
            if isinstance(arg, Rational):
                a = arg.p
                b = arg.q
                res = k(a) / k(b)
            else:
                res = resolve(arg, k)
            args.append(res)
        return expression.func(*args)

    expr = resolve(expr, k)
    poly = Poly(expr, symbols(param), domain=k)
    roots = poly.ground_roots()
    for root in roots:
        params[param] = int(root)
        break


if __name__ == "__main__":
    start = datetime.now()
    for _ in range(1000):
        do_thing()
    end = datetime.now()
    print("This took", end - start)
