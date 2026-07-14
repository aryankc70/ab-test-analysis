"""Design and analyze a simulated marketing A/B test."""
import numpy as np
from scipy import stats
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize, proportions_ztest, confint_proportions_2indep

rng = np.random.default_rng(42)

# ---- 1. Design: how many users do we need? ----
BASELINE, MDE = 0.10, 0.02          # 10% conversion, want to detect +2pp
effect = proportion_effectsize(BASELINE + MDE, BASELINE)
n_per_arm = int(np.ceil(NormalIndPower().solve_power(effect, alpha=0.05, power=0.8)))
print(f"Required sample size: {n_per_arm:,} per arm "
      f"(baseline {BASELINE:.0%}, MDE {MDE:.0%}, power 0.8)")

# ---- 2. Simulate the experiment (true lift = +2.5pp) ----
control = rng.binomial(1, 0.100, n_per_arm)
treat   = rng.binomial(1, 0.125, n_per_arm)

# ---- 3. Sanity check: sample ratio mismatch ----
srm_p = stats.chisquare([len(control), len(treat)]).pvalue
print(f"SRM check p={srm_p:.3f} ({'OK' if srm_p > 0.01 else 'FAIL — investigate assignment'})")

# ---- 4. Analyze ----
succ = np.array([treat.sum(), control.sum()])
n = np.array([len(treat), len(control)])
z, p = proportions_ztest(succ, n)
lo, hi = confint_proportions_2indep(succ[0], n[0], succ[1], n[1])
lift = treat.mean() - control.mean()

print(f"\nControl: {control.mean():.3%}   Treatment: {treat.mean():.3%}")
print(f"Lift: {lift:+.2%}  (95% CI [{lo:+.2%}, {hi:+.2%}])  z={z:.2f}  p={p:.4f}")

# ---- 5. Plain-language memo ----
verdict = ("SHIP: statistically significant improvement" if p < 0.05 and lift > 0
           else "DO NOT SHIP yet: result not significant")
memo = f"""# Experiment Results Memo

**Question:** Does the new landing page increase signup conversion?

**Design:** {n_per_arm:,} users per arm, randomized 50/50, powered to detect a 2pp lift.

**Result:** Treatment converted at {treat.mean():.1%} vs control {control.mean():.1%} —
a lift of {lift:+.1%} (95% CI [{lo:+.1%}, {hi:+.1%}], p={p:.4f}).

**Recommendation:** {verdict}.
"""
open("results_memo.md", "w").write(memo)
print("\n" + memo)
