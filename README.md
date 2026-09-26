# Selling the Suspense: Terminal-Uncertainty Resolution and Price Reversal in Sports Collectible Markets

Data and code accompanying the abstract submitted to the MIT Sloan Sports
Analytics Conference (SSAC27) Research Paper Competition.

## What this repository contains

This repo supports the abstract's empirical claims with the underlying
transaction-level data and the code used to compute every statistic cited
in the Results section. It does **not** contain any proprietary business
data — every price point below comes from public secondary-market card
sales (eBay, Fanatics, Goldin) as aggregated by [Card Ladder](https://cardladder.com),
a third-party sports-card price-tracking service. Proprietary trading data
from the authors' own collectibles business is used only in later stages
of this research program (the decision-focused trading-strategy comparison
planned for the full manuscript) and is not part of this abstract's
evidence base.

## Repository structure

```
data/           Raw transaction-level CSVs, one per card/event studied
scripts/        Code that recomputes every reported statistic from the raw CSVs
README.md       This file
LICENSE         MIT license (code); data is republished public sale records
```

## Data files (`data/`)

Each CSV is a set of individual card sales (date, price, platform, seller)
for one specific card (player, set, parallel, grade) around one resolution
event, with a `Days Relative to <event>` column marking each sale as
before (negative), on (zero), or after (positive) the day the relevant
uncertainty was resolved.

| File | Card | Event |
|---|---|---|
| `tatum_2024_base_prizm.csv` | 2017 Panini Prizm Jayson Tatum #16 (Base, PSA 10) | 2024 NBA Championship (Jun 17, 2024) |
| `sga_2025_silver_prizm.csv` | 2018 Panini Prizm Shai Gilgeous-Alexander #184 (Silver, PSA 10) | 2025 NBA Championship, Game 7 (Jun 22, 2025) |
| `brown_2024_base_prizm.csv` | 2016 Panini Prizm Jaylen Brown #44 (Base, PSA 10) | 2024 NBA Championship + Finals MVP (Jun 17, 2024) |
| `haliburton_2025_ecf_clinch.csv` | 2020 Panini Prizm Tyrese Haliburton #262 (Silver, PSA 10) | 2025 Eastern Conference Finals clinch (May 31, 2025) — a **partial**-resolution event (advanced to the Finals; the championship question itself remained open) |
| `tatum_2024_full_timeline.csv` | Same Tatum card as above | Full 2024 title run, regular season through the championship (narrative-stage labels instead of a single event date) |
| `sga_2025_full_timeline.csv` | Same SGA card as above | Full 2025 title run, regular season through Game 7 |
| `tatum_2024_silver_extended.csv` | 2017 Panini Prizm Jayson Tatum #16 (**Silver** parallel, PSA 10) | 2024 Championship, extended through the 2024-25 season start — a liquidity-tier robustness check against the Base-parallel result above |
| `sga_2025_silver_extended.csv` | Same SGA Silver card as above | 2025 Championship, extended through the 2025-26 season start |

All prices are individual, dated secondary-market sale records, not index
values or asking prices. Sale platform and (where visible in the public
listing) seller handle are recorded for traceability; sales pulled from a
platform that did not expose a seller handle are marked accordingly.

## Reproducing the paper's numbers

```bash
cd scripts
python3 compute_stage_averages.py
```

This recomputes, directly from the CSVs, the pre-resolution average price,
the resolution-day average, the post-resolution average, and the
percentage change for every event file — independent of any spreadsheet
formula, i.e. this is the ground truth for the numbers quoted in the
paper. Sample output:

```
file                                    n_pre    avg_pre  n_day0   avg_day0  n_post   avg_post     %chg
----------------------------------------------------------------------------------------------------
brown_2024_base_prizm.csv                   4     162.25       5     173.50      18     118.82   -26.8%
haliburton_2025_ecf_clinch.csv              6     382.91       2     425.00      10     385.90    +0.8%
sga_2025_silver_prizm.csv                   8   1,064.75       3   1,109.90      13   1,023.04    -3.9%
tatum_2024_base_prizm.csv                   4     134.88       4     132.52      37     113.96   -15.5%
```

(The paper's finer-grained staged breakdown — e.g. day 1-30 vs. day 31-60
vs. new-season-start averages for the extended timelines — uses the same
`Days Relative` column with narrower cutoffs; see the full-timeline and
extended CSVs, which include a `Narrative Stage` / date column for exactly
this purpose.)

## Data collection method

Sales were identified on Card Ladder Pro (a paid card-price-tracking
subscription) by filtering each card's public sale history to a date
window bracketing the relevant resolution event, and recording every
listed sale in that window. No sales were excluded except exact duplicate
listings. Card Ladder itself sources these records from eBay, Fanatics
Collect, and Goldin's public sold-listing data.

## Known limitations (see paper for full discussion)

- Sample size: this is a starting event-study sample (4-5 players, several
  hundred individual transactions across 8 event-windows), not a large-N
  systematic sample.
- A parallel cross-category test (2022 FIFA World Cup Final, Lionel Messi)
  did not replicate the direction of the NBA-based effect; see the paper's
  Conclusion for discussion. That dataset is not included in this initial
  repository and will be added alongside the full manuscript.
- Card tier affects the magnitude of the effect (compare the Base-parallel
  and Silver-parallel files for the same players/events); the paper
  reports this as a robustness dimension, not a nuisance to be averaged
  away.

## Citation

If you use this data, please cite the abstract (full citation to be added
upon acceptance) and, per Card Ladder's terms, credit Card Ladder Pro as
the underlying data aggregator.
