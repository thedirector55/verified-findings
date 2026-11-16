# SciPy: `poisson_means_test` accepts an upper-case `alternative` and silently runs the wrong test

- **Software:** SciPy, `scipy.stats.poisson_means_test`
- **Checked on:** 2026-11-16, SciPy 1.18.1 with NumPy 2.5.4, Python 3.12.10, Windows 11. Source also read on `main` at commit `8c3fce06ad1d96806fb88cd85b6d66d2fa5175b6`.
- **Upstream status:** not reported. Searches of the SciPy tracker for `poisson_means_test` with `alternative`, `case`, `uppercase` and `lower` on 2026-11-16 found no matching issue.
- **AI disclosure:** found by AI models during a wider audit; this write-up and the script are AI-written.

## What goes wrong

`alternative='LESS'`, `'Less'` or `'TWO-SIDED'` passes input validation, raises no error, and returns the p-value of the `'greater'` test.

Output of `repro_alternative_case.py` on SciPy 1.18.1, for `poisson_means_test(6, 10, 2, 10, alternative=...)`:

```
alternative='less'       p = 0.927561
alternative='LESS'       p = 0.087437
alternative='Less'       p = 0.087437
alternative='two-sided'  p = 0.174875
alternative='TWO-SIDED'  p = 0.087437
alternative='greater'    p = 0.087437
alternative='GREATER'    p = 0.087437
```

A user who writes `'LESS'` gets 0.087 where the one-sided "less" p-value is 0.928.

## How to run

```
python repro_alternative_case.py
```

## Cause, from reading the source

In `scipy/stats/_hypotests.py` the validation lower-cases the argument:

```python
alternatives = {'two-sided', 'less', 'greater'}
if alternative.lower() not in alternatives:
    raise ValueError(f"Alternative must be one of '{alternatives}'.")
```

but the branch that selects the test compares the original string:

```python
if alternative == 'two-sided':
    indicator = np.abs(t_x1x2) >= np.abs(t_k1k2)
elif alternative == 'less':
    indicator = t_x1x2 <= t_k1k2
else:
    indicator = t_x1x2 >= t_k1k2
```

Any accepted spelling that is not exactly `'two-sided'` or `'less'` falls into the `else` branch, which is the `'greater'` test. Both snippets are present on `main` at the commit above.

## How other SciPy tests handle the same input

On SciPy 1.18.1, with `'LESS'` and `'TWO-SIDED'`:

- `mannwhitneyu`, `wilcoxon` and `ks_2samp` accept upper case and return the same result as lower case.
- `ttest_ind`, `fisher_exact`, `barnard_exact`, `boschloo_exact`, `binomtest` and `pearsonr` raise `ValueError`.
- Of the ten functions tried, only `poisson_means_test` accepts the string and returns a different test's result.

## Limits of this entry

- The documentation lists only the lower-case spellings, so a caller following the documentation is not affected.
- No fix is proposed here. Either normalising the string once or rejecting non-lower-case input would remove the mismatch.
