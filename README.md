# A/B Test Design & Analysis

End-to-end experiment workflow: power analysis → simulated randomized experiment → sanity checks → significance testing → plain-language results memo.

## Quickstart
```bash
pip install -r requirements.txt
python analysis.py
```
Outputs a full experiment report to stdout and `results_memo.md`.

## What it covers
- Sample size via power analysis (α=0.05, power=0.8, MDE=2pp)
- SRM (sample-ratio mismatch) check before reading results
- Two-proportion z-test + confidence interval for the lift
- Business translation: "what should we ship, and how sure are we?"

## Sample output

Required sample size: 3,835 per arm (baseline 10%, MDE 2%, power 0.8)
SRM check p=1.000 (OK)

Control: 10.169%   Treatment: 11.864%
Lift: +1.69%  (95% CI [+0.29%, +3.10%])  z=2.37  p=0.0178

**Decision: SHIP — statistically significant improvement.** The confidence
interval excludes zero, and the SRM check confirms randomization was healthy
before reading any results.

## Power sensitivity experiment

I re-ran the analysis with MDE raised from 2pp to 3pp:

| MDE | Required n/arm | Observed lift | p-value | Decision |
|---|---|---|---|---|
| 2pp | 3,835 | +1.69% | 0.0178 | SHIP |
| 3pp | 1,769 | +1.92% | 0.0711 | DO NOT SHIP |

Same underlying effect, opposite conclusions. The 3pp design halves the
sample size but is underpowered for a ~2pp true effect — the observed lift
was even *larger* in the second run, yet the confidence interval crossed
zero. Takeaway: choosing MDE is a business decision about the smallest
effect worth acting on, and underpowering silently converts real wins
into "no result."