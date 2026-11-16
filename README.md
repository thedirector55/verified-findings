# Verified findings

Defects found in public software and reference material, each with a script anyone can run to see the problem.

## How this work is done, and what "verified" means here

- I run AI models (Claude and others) to test public libraries against exact reference answers: exact fractions, a second independent implementation, or a much higher-precision calculation.
- **The write-ups and scripts in this repository are AI-written.** I am not a specialist in the internals of these libraries.
- An entry is listed only when its reproducer has been run on my machine against a released version of the software, the output is saved next to it, and the upstream tracker has been searched for an existing report. The date and versions are stated in each entry.
- "Verified" means exactly that: the script ran and printed what the entry says. It does not mean a maintainer has confirmed the defect. Where a maintainer has responded, the entry says so.
- If an entry is wrong, please open an issue here. Wrong entries are corrected in place and the correction is kept visible.

## Entries

| Entry | Software | What goes wrong | Checked on | Upstream status |
|---|---|---|---|---|
| [mpmath-iv-log-enclosure](findings/mpmath-iv-log-enclosure/) | mpmath 1.4.1 and master | `iv.log(1 + 2**-(p-1))` returns a point interval that lies below the true value | 2026-11-16 | Not reported. Same class as mpmath issue 1181 (`mpf_exp`) |
| [scipy-poisson-means-test-alternative-case](findings/scipy-poisson-means-test-alternative-case/) | SciPy 1.18.1 and main | `poisson_means_test(..., alternative='LESS')` is accepted and silently runs the `'greater'` test | 2026-11-16 | Not reported |

## Licence

Scripts are under the MIT licence (see `LICENSE`). Text is free to quote with attribution.
