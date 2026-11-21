"""Simulation: would route-based delivery promises beat today's? Fit on orders bought in 2016-2017,
test on orders bought in 2018. A route is seller state to customer state. Routes with fewer than 30
training orders fall back to the customer state, then to all orders. Promise = the chosen percentile of
past delivery days, rounded up. Writes data/simulation.json."""
import json, gzip, shutil, sqlite3, tempfile
import numpy as np, pandas as pd
tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False).name
shutil.copyfileobj(gzip.open("data/olist.db.gz"), open(tmp, "wb"))
con = sqlite3.connect(tmp)
d = pd.read_sql("""SELECT o.order_id, o.state AS cs, s.state AS ss, o.purchased_at, o.delivered_at, o.estimated_at
  FROM orders o JOIN (SELECT order_id, MIN(seller_id) AS seller_id FROM items GROUP BY order_id) i USING (order_id)
  JOIN sellers s USING (seller_id) WHERE o.delivered_at IS NOT NULL""", con)
for c in ["purchased_at", "delivered_at", "estimated_at"]: d[c] = pd.to_datetime(d[c])
d["days"] = (d.delivered_at - d.purchased_at).dt.days; d["prom"] = (d.estimated_at - d.purchased_at).dt.days
tr, te = d[d.purchased_at < "2018-01-01"], d[d.purchased_at >= "2018-01-01"]
n = tr.groupby(["ss", "cs"]).size().rename("n")
rows = [{"rule": "Today's promise", "promise_days": round(te.prom.mean(), 1), "pct_late": round((te.days > te.prom).mean() * 100, 1)}]
for k in [2, 3]:
    rows.append({"rule": f"Today's promise minus {k} days", "promise_days": round((te.prom - k).mean(), 1), "pct_late": round((te.days > te.prom - k).mean() * 100, 1)})
for p in [0.90, 0.92, 0.93, 0.94, 0.95]:
    q = tr.groupby(["ss", "cs"]).days.quantile(p).rename("q"); qs = tr.groupby("cs").days.quantile(p).rename("qs"); qa = tr.days.quantile(p)
    t = te.join(q, on=["ss", "cs"]).join(n, on=["ss", "cs"]).join(qs, on="cs")
    t["newp"] = np.ceil(np.where(t.n >= 30, t.q, np.where(t.qs.notna(), t.qs, qa)))
    rows.append({"rule": f"Route-based, {int(p * 100)}th percentile", "promise_days": round(t.newp.mean(), 1), "pct_late": round((t.days > t.newp).mean() * 100, 1)})
res = {"train_orders": len(tr), "test_orders": len(te), "routes_with_30_plus": int((n >= 30).sum()), "rows": rows}
json.dump(res, open("data/simulation.json", "w"), indent=1)
print(json.dumps(res, indent=1))
