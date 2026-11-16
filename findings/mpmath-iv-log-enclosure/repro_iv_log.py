"""iv.log(1 + 2**-(p-1)) at precision p returns a point interval that excludes the true value."""
import mpmath
from mpmath import iv, mp, mpf

print("mpmath", mpmath.__version__)
for p in (24, 53, 64, 113, 200):
    iv.prec = p
    x = iv.mpf(1) + iv.mpf(2) ** (-(p - 1))      # exactly representable: 1 + 2^-(p-1)
    assert x.a == x.b
    r = iv.log(x)
    mp.prec = 8 * p                               # reference at much higher precision
    t = mp.log(mpf(1) + mpf(2) ** (-(p - 1)))
    lo, hi = mpf(r.a), mpf(r.b)
    print(f"prec={p:3}  [{mp.nstr(lo, 20)}, {mp.nstr(hi, 20)}]  width={mp.nstr(hi - lo, 3)}"
          f"  true-hi={mp.nstr(t - hi, 3)}  contains true value: {lo <= t <= hi}")
