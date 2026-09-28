"""Reproduces Table 1 and the robustness checks cited in the SSAC27 abstract.
Run from the repo's scripts/ folder:  python3 statistical_tests.py
Requires: scipy
"""
import csv, os, random
from collections import defaultdict
from scipy import stats

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
CASES = {"Tatum": "tatum_2024_base_prizm.csv", "SGA": "sga_2025_silver_prizm.csv",
         "Brown": "brown_2024_base_prizm.csv", "Haliburton ECF": "haliburton_2025_ecf_clinch.csv"}

def load(f):
    rows = list(csv.DictReader(open(os.path.join(DATA, f), encoding="utf-8")))
    dc = [k for k in rows[0] if k.startswith("Days Relative")][0]
    out = []
    for r in rows:
        try: out.append((int(r[dc]), float(r["Price (USD)"])))
        except (KeyError, ValueError): pass
    return out

D = {k: load(v) for k, v in CASES.items()}
split = lambda d: ([p for t, p in d if t < 0], [p for t, p in d if t > 0])
mean = lambda x: sum(x) / len(x)

def norm(d):  # percent deviation from the case's own pre-event mean
    m = mean(split(d)[0]); return [(t, (p - m) / m * 100) for t, p in d]

print("Table 1 (two-sided Welch on individual transactions)")
for k, d in D.items():
    pre, post = split(d); t, p = stats.ttest_ind(post, pre, equal_var=False)
    print(f"{k:15s} n={len(pre)}/{len(post)} pre={mean(pre):.2f} post={mean(post):.2f} chg={(mean(post)/mean(pre)-1)*100:+.1f}% t={t:.2f} p={p:.4f}")

pool = norm(D["Tatum"]) + norm(D["SGA"])
pre = [x for t, x in pool if t < 0]; post = [x for t, x in pool if t > 0]
t, p = stats.ttest_ind(post, pre, equal_var=False, alternative="less")
print(f"\nPooled titles (one-sided): n={len(pre)}/{len(post)} t={t:.2f} p={p:.5f}")

by = defaultdict(list)
for c in ("Tatum", "SGA"):
    for t_, x in norm(D[c]): by[(c, t_)].append(x)
dpre = [mean(v) for (c, t_), v in by.items() if t_ < 0]; dpost = [mean(v) for (c, t_), v in by.items() if t_ > 0]
t, p = stats.ttest_ind(dpost, dpre, equal_var=False, alternative="less")
print(f"Day-level aggregation: days={len(dpre)}/{len(dpost)} t={t:.2f} p={p:.4f}")

random.seed(1); N = 20000
diff = lambda s: mean([x for t_, x in s if t_ > 0]) - mean([x for t_, x in s if t_ < 0])
obs = diff(pool); cases = [norm(D["Tatum"]), norm(D["SGA"])]; hit = 0
for _ in range(N):
    sh = []
    for c in cases:
        ts = [t_ for t_, _ in c]; xs = [x for _, x in c]; random.shuffle(xs); sh += list(zip(ts, xs))
    hit += diff(sh) <= obs
print(f"Permutation test (labels shuffled within case): obs={obs:.2f} p={(hit+1)/(N+1):.4f}")

bt = [x for t_, x in norm(D["Brown"]) if t_ > 0]; tt = [x for t_, x in norm(D["Tatum"]) if t_ > 0]
t, p = stats.ttest_ind(bt, tt, equal_var=False, alternative="less")
print(f"Brown vs Tatum post-decline (one-sided): t={t:.2f} p={p:.4f}")
