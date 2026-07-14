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
