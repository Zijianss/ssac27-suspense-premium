"""
Reproduces the pre-/post-resolution price statistics reported in the paper
directly from the raw transaction-level CSVs in ../data/.

Each event-study CSV has a "Days Relative to <event>" column (negative =
before the resolution date, 0 = resolution day, positive = after).
This script recomputes the group averages and % changes from that column,
independent of any cached spreadsheet formulas -- i.e. it is the ground
truth for every number cited in the paper's Results section.

Usage:
    python3 compute_stage_averages.py
"""

import csv
import glob
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def load_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def find_days_column(fieldnames):
    for name in fieldnames:
        if name and name.startswith("Days Relative"):
            return name
    return None


def summarize(path):
    rows = load_rows(path)
    if not rows:
        return None
    days_col = find_days_column(rows[0].keys())
    if days_col is None:
        return None  # not an event-study file (e.g. a full timeline with a "Narrative Stage" column instead)

    pre, event_day, post = [], [], []
    for r in rows:
        try:
            price = float(r["Price (USD)"])
            days = int(r[days_col])
        except (KeyError, ValueError):
            continue
        if days < 0:
            pre.append(price)
        elif days == 0:
            event_day.append(price)
        else:
            post.append(price)

    def avg(xs):
        return sum(xs) / len(xs) if xs else None

    pre_avg, event_avg, post_avg = avg(pre), avg(event_day), avg(post)
    pct_change = (post_avg - pre_avg) / pre_avg if pre_avg and post_avg else None

    return {
        "file": os.path.basename(path),
        "n_pre": len(pre), "avg_pre": pre_avg,
        "n_event_day": len(event_day), "avg_event_day": event_avg,
        "n_post": len(post), "avg_post": post_avg,
        "pct_change_pre_to_post": pct_change,
    }


def main():
    paths = sorted(glob.glob(os.path.join(DATA_DIR, "*.csv")))
    print(f"{'file':38s} {'n_pre':>6s} {'avg_pre':>10s} {'n_day0':>7s} {'avg_day0':>10s} {'n_post':>7s} {'avg_post':>10s} {'%chg':>8s}")
    print("-" * 100)
    for path in paths:
        s = summarize(path)
        if s is None:
            continue
        fmt = lambda x: f"{x:,.2f}" if x is not None else "n/a"
        pct = f"{s['pct_change_pre_to_post']*100:+.1f}%" if s["pct_change_pre_to_post"] is not None else "n/a"
        print(f"{s['file']:38s} {s['n_pre']:6d} {fmt(s['avg_pre']):>10s} {s['n_event_day']:7d} {fmt(s['avg_event_day']):>10s} {s['n_post']:7d} {fmt(s['avg_post']):>10s} {pct:>8s}")


if __name__ == "__main__":
    main()
