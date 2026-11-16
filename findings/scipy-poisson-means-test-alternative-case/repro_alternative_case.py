"""scipy.stats.poisson_means_test: an upper-case `alternative` is accepted but runs the 'greater' test."""
import scipy
from scipy import stats

print("scipy", scipy.__version__)
args = (6, 10, 2, 10)   # k1, n1, k2, n2
for alt in ("less", "LESS", "Less", "two-sided", "TWO-SIDED", "greater", "GREATER"):
    print(f"alternative={alt!r:12} p = {stats.poisson_means_test(*args, alternative=alt).pvalue:.6f}")
