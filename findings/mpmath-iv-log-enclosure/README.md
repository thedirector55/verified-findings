# mpmath: `iv.log` returns an interval that excludes the true value for inputs just above 1

- **Software:** mpmath, interval context (`iv`)
- **Checked on:** 2026-11-16, mpmath 1.4.1 (PyPI) and master at commit `c5ce6bebebd7a17295f4d8f49379d2e57cd5eabe` (1.5.0a3.dev17), Python 3.12.10, Windows 11
- **Upstream status:** not reported. A search of the mpmath tracker for `iv.log`, `mpi_log` and `mpf_ln rounding` on 2026-11-16 found no issue with a concrete `log` example. Issue [1181](https://github.com/mpmath/mpmath/issues/1181) covers the same kind of problem for `mpf_exp`, and a comment there mentions `mpf_ln` mismatches in aggregate without an input.
- **AI disclosure:** found by AI models testing against a high-precision reference; this write-up and the script are AI-written.

## What goes wrong

With working precision `p` bits, take `x = 1 + 2**-(p-1)`, which is exactly representable. `iv.log(x)` returns an interval whose two endpoints are equal, and that single value is below `log(x)`. The true value is not in the returned interval.

At the default 53 bits:

```
x      = 1 + 2**-52
iv.log = [2.2204460492503128343e-16, 2.2204460492503128343e-16]   (width 0)
true   = 2.2204460492503128343e-16 + 3.65e-48
```

The same happens at 24, 64, 113 and 200 bits. See `output_mpmath_1.4.1.txt` and `output_mpmath_master_c5ce6beb.txt`.

## How to run

```
python repro_iv_log.py
```

The script needs only mpmath. For each precision it builds `x`, calls `iv.log`, computes a reference with `mp.log` at eight times the precision, and prints whether the reference lies inside the returned interval.

## How far it extends

At 53 bits:

- Of the 2,000 inputs `1 + k * 2**-52` for `k = 1..2000`, 63 fail: `k = 1, 2, 4, 8, 12, 16, 24, 32, 40, 48, ...`
- `1 + 2**-51` and `1 + 2**-40` fail. `1 + 3 * 2**-52`, `1 - 2**-52`, `1 + 2**-30`, `1.5` and `2` do not.
- 20,000 random 53-bit inputs with exponents from -60 to 60: none fail.

So the failures are confined to inputs very close to 1.

The numerical error itself is tiny, about `eps**3 / 3` with `eps = x - 1`, far below one unit in the last place. The defect is the direction: the endpoint computed with rounding towards plus infinity is below the true value.

## Cause, from reading the source

`mpi_log` in `mpmath/libmp/libmpi.py` is

```python
a = mpf_ln(sa, prec, round_floor)
b = mpf_ln(sb, prec, round_ceiling)
```

In `mpf_ln` (`mpmath/libmp/libelefun.py`), inputs close to 1 take the branch that calls `log_taylor` in fixed point with `wp = prec + 20 + cancellation` bits and then `from_man_exp(s, -wp, prec, rnd)`.

For `x = 1 + eps` with `eps = 2**-52` and `prec = 53`, `wp` is 125 bits. The series is `eps - eps**2/2 + eps**3/3 - ...`. The third term is about `2**-157.6`, below the fixed-point resolution, so the fixed-point result is exactly `eps - eps**2/2`. That number, `2**-52 * (1 - 2**-53)`, has a 53-bit mantissa and is exactly representable at the target precision. `from_man_exp` then has nothing to round in either direction, so floor and ceiling both return it:

```
mpf_ln(x, 53, round_ceiling) == mpf_ln(x, 53, round_floor) == (0, 9007199254740991, -105, 53)
```

In other words the directed rounding is applied to a truncated value as if it were exact. The neighbouring branch for `cancellation > wp` does call `mpf_perturb` to account for this; the Taylor branch does not.

## Limits of this entry

- mpmath's documentation says interval support is experimental, and in issue 1181 a maintainer states that elementary functions guarantee full accuracy but not correct directed rounding. This entry is a concrete example of that known gap for `log`, with its cause. It is not a new class of defect.
- No fix is proposed here.
