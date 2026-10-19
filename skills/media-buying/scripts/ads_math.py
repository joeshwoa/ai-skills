#!/usr/bin/env python3
"""Paid-media arithmetic an agent should never do in its head.

Subcommands (all print JSON):
  metrics    --spend S --impressions I --clicks C --conversions N [--revenue R] [--reach U]
  breakeven  --price P --cogs C [--other-var V] [--cod-delivery-rate 0.7] [--return-rate 0.1]
  budget     --target-cpa A --conversions-needed N [--days D]      # budget to buy N conversions at A
  test-size  --cpa A [--variants 3] [--events-per-variant 50]      # minimum test budget
  abtest     --a-n N --a-x X --b-n N --b-x X                       # two-proportion z-test (CTR/CVR)
  scale      --budget B --step 0.2 --steps 5                       # staged budget increases
  pacing     --budget-total B --spent S --days-total D --days-elapsed E
  cod        --orders N --delivered-rate 0.7 --aov V --spend S     # real ROAS under cash-on-delivery
Money is in whatever currency you pass; nothing is converted.
"""
import argparse, json, math

def sd(a, b): return a / b if b else None
def r(x, n=4): return None if x is None else round(x, n)

def metrics(a):
    o = {"CPM": r(sd(a.spend * 1000, a.impressions)), "CTR": r(sd(a.clicks, a.impressions)),
         "CPC": r(sd(a.spend, a.clicks)), "CVR_click": r(sd(a.conversions, a.clicks)),
         "CPA": r(sd(a.spend, a.conversions))}
    if a.revenue is not None:
        o["ROAS"] = r(sd(a.revenue, a.spend)); o["AOV"] = r(sd(a.revenue, a.conversions))
    if a.reach: o["frequency"] = r(sd(a.impressions, a.reach))
    return o

def breakeven(a):
    margin = a.price - a.cogs - a.other_var
    if margin <= 0: return {"error": "non-positive unit margin", "unit_margin": margin}
    eff = a.cod_delivery_rate * (1 - a.return_rate)
    # a paid order only becomes profit if delivered and kept; margin is earned per kept order,
    # while the ad spend is paid per order placed.
    be_cpa = margin * eff
    return {"unit_margin": r(margin, 2), "kept_order_rate": r(eff),
            "breakeven_CPA_per_order": r(be_cpa, 2),
            "breakeven_ROAS_on_order_value": r(sd(a.price, be_cpa), 2),
            "note": "CPA/ROAS reported by the ad platform counts orders placed; use these break-even numbers against platform figures"}

def budget(a):
    total = a.target_cpa * a.conversions_needed
    o = {"total_budget": r(total, 2)}
    if a.days: o["per_day"] = r(total / a.days, 2)
    return o

def test_size(a):
    per = a.cpa * a.events_per_variant
    return {"per_variant": r(per, 2), "total": r(per * a.variants, 2),
            "reason": "about %d optimization events per variant are needed before differences are more than noise" % a.events_per_variant}

def abtest(a):
    p1, p2 = a.a_x / a.a_n, a.b_x / a.b_n
    p = (a.a_x + a.b_x) / (a.a_n + a.b_n)
    se = math.sqrt(p * (1 - p) * (1 / a.a_n + 1 / a.b_n))
    z = (p2 - p1) / se if se else 0.0
    pv = math.erfc(abs(z) / math.sqrt(2))
    return {"rate_a": r(p1, 5), "rate_b": r(p2, 5), "lift_b_vs_a": r(sd(p2 - p1, p1)), "z": r(z, 3),
            "p_value_two_sided": r(pv, 4),
            "verdict": "difference likely real (p<0.05)" if pv < 0.05 else "not significant: keep running or treat as equal"}

def scale(a):
    out, b = [], a.budget
    for i in range(a.steps):
        b = b * (1 + a.step); out.append(r(b, 2))
    return {"schedule": out, "rule": "heuristic, not a platform rule: raise by this step at most every 3-4 days, only while CPA stays within 20% of target; hold if it breaks"}

def pacing(a):
    exp = a.budget_total * a.days_elapsed / a.days_total
    return {"expected_spend": r(exp, 2), "actual": a.spent, "deviation_pct": r(sd(a.spent - exp, exp) * 100, 1) if exp else None,
            "daily_budget_to_land_total": r(sd(a.budget_total - a.spent, a.days_total - a.days_elapsed), 2)}

def cod(a):
    delivered = a.orders * a.delivered_rate
    rev_booked, rev_real = a.orders * a.aov, delivered * a.aov
    return {"platform_ROAS": r(sd(rev_booked, a.spend), 2), "real_ROAS_delivered": r(sd(rev_real, a.spend), 2),
            "platform_CPA": r(sd(a.spend, a.orders), 2), "real_CPA_per_delivered": r(sd(a.spend, delivered), 2)}

ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
def add(name, fn, *args):
    s = sp.add_parser(name); s.set_defaults(fn=fn)
    for flag, kw in args: s.add_argument(flag, **kw)
F = dict(type=float, required=True)
add("metrics", metrics, ("--spend", F), ("--impressions", F), ("--clicks", F), ("--conversions", F),
    ("--revenue", dict(type=float)), ("--reach", dict(type=float)))
add("breakeven", breakeven, ("--price", F), ("--cogs", F), ("--other-var", dict(type=float, default=0.0)),
    ("--cod-delivery-rate", dict(type=float, default=1.0)), ("--return-rate", dict(type=float, default=0.0)))
add("budget", budget, ("--target-cpa", F), ("--conversions-needed", F), ("--days", dict(type=float)))
add("test-size", test_size, ("--cpa", F), ("--variants", dict(type=int, default=3)), ("--events-per-variant", dict(type=int, default=50)))
add("abtest", abtest, ("--a-n", F), ("--a-x", F), ("--b-n", F), ("--b-x", F))
add("scale", scale, ("--budget", F), ("--step", dict(type=float, default=0.2)), ("--steps", dict(type=int, default=5)))
add("pacing", pacing, ("--budget-total", F), ("--spent", F), ("--days-total", F), ("--days-elapsed", F))
add("cod", cod, ("--orders", F), ("--delivered-rate", dict(type=float, default=0.7)), ("--aov", F), ("--spend", F))
a = ap.parse_args()
print(json.dumps(a.fn(a), indent=1))
