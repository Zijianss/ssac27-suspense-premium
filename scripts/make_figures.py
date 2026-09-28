"""Regenerates Figure 1 (event-time price paths) and Table 1 (results) for the abstract.
Run from the scripts/ folder:  python3 make_figures.py   -> writes ../figures/
Requires: matplotlib, scipy
"""
import csv, os
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

HERE = os.path.dirname(__file__)
DATA, OUT = os.path.join(HERE, "..", "data"), os.path.join(HERE, "..", "figures")
os.makedirs(OUT, exist_ok=True)

def load(f):
    rows = list(csv.DictReader(open(os.path.join(DATA, f), encoding="utf-8")))
    dc = [k for k in rows[0] if k.startswith("Days Relative")][0]
    out = []
    for r in rows:
        try: out.append((int(r[dc]), float(r["Price (USD)"])))
        except (KeyError, ValueError): pass
    return out

mean = lambda x: sum(x) / len(x)
CASES = [("Tatum, 2024 title", "tatum_2024_base_prizm.csv", "#1f4e79"),
         ("Gilgeous-Alexander, 2025 title", "sga_2025_silver_prizm.csv", "#2e8b57"),
         ("Brown, 2024 title + Finals MVP", "brown_2024_base_prizm.csv", "#c0392b"),
         ("Haliburton, 2025 conf.-finals win", "haliburton_2025_ecf_clinch.csv", "#7f6a93")]

def path_index(d):
    m = mean([p for t, p in d if t < 0]); by = defaultdict(list)
    for t, p in d: by[t].append(p / m * 100)
    days = sorted(by); return days, [mean(by[t]) for t in days]

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6), sharey=True,
                             gridspec_kw={"wspace": 0.08, "width_ratios": [1.6, 1]})
for i, (name, f, c) in enumerate(CASES):
    d, y = path_index(load(f)); (a1 if i < 3 else a2).plot(d, y, marker="o", ms=4, lw=1.6, color=c, label=name)
for a, t in ((a1, "Terminal resolution: title decided"), (a2, "Partial resolution: title still open")):
    a.axvline(0, color="#444", ls="--", lw=1); a.axhline(100, color="#bbb", lw=0.8)
    a.set_title(t, loc="left"); a.set_xlabel("Days relative to resolution"); a.legend(frameon=False, loc="lower left")
a1.set_ylabel("Mean daily sale price (pre-event mean = 100)")
fig.savefig(os.path.join(OUT, "Figure1_event_time_prices.png"), dpi=200, bbox_inches="tight")

rows = []
for name, f, _ in CASES:
    d = load(f); pre = [p for t, p in d if t < 0]; post = [p for t, p in d if t > 0]
    t, p = stats.ttest_ind(post, pre, equal_var=False)
    rows.append([name, f"{len(pre)} / {len(post)}", f"{mean(pre):,.2f}", f"{mean(post):,.2f}",
                 f"{(mean(post) / mean(pre) - 1) * 100:+.1f}%", f"{t:.2f}", f"{p:.3f}"])
fig, ax = plt.subplots(figsize=(11, 2.6)); ax.axis("off")
tb = ax.table(cellText=rows, colLabels=["Case", "n pre/post", "Pre ($)", "Post ($)", "Change", "Welch t", "p (two-sided)"],
              loc="center", cellLoc="center", colWidths=[.34, .12, .12, .12, .10, .10, .10])
tb.auto_set_font_size(False); tb.set_fontsize(10); tb.scale(1, 1.6)
fig.savefig(os.path.join(OUT, "Table1_results.png"), dpi=200, bbox_inches="tight")
print("Wrote figures to", os.path.abspath(OUT))
