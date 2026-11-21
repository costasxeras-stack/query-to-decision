"""Builds data/olist.db (SQLite) from the Olist CSVs in work/. Long hash ids become short integers,
review text and payments are dropped, and only the columns the analysis uses are kept. Then gzips it for the browser."""
import sqlite3, gzip, shutil, os, pandas as pd
W = "work"
o = pd.read_csv(f"{W}/olist_orders_dataset.csv"); c = pd.read_csv(f"{W}/olist_customers_dataset.csv")
it = pd.read_csv(f"{W}/olist_order_items_dataset.csv"); r = pd.read_csv(f"{W}/olist_order_reviews_dataset.csv")
p = pd.read_csv(f"{W}/olist_products_dataset.csv"); s = pd.read_csv(f"{W}/olist_sellers_dataset.csv")
pay = pd.read_csv(f"{W}/olist_order_payments_dataset.csv"); tr = pd.read_csv(f"{W}/product_category_name_translation.csv")
def ids(series): return {v: i + 1 for i, v in enumerate(pd.unique(series))}
oid = ids(o.order_id); cid = ids(c.customer_unique_id); pid = ids(p.product_id); sid = ids(s.seller_id)
c2 = c.set_index("customer_id")
orders = pd.DataFrame({"order_id": o.order_id.map(oid), "customer_id": o.customer_id.map(c2.customer_unique_id).map(cid),
  "state": o.customer_id.map(c2.customer_state), "status": o.order_status,
  "purchased_at": o.order_purchase_timestamp, "shipped_at": o.order_delivered_carrier_date,
  "delivered_at": o.order_delivered_customer_date, "estimated_at": o.order_estimated_delivery_date})
items = pd.DataFrame({"order_id": it.order_id.map(oid), "item_no": it.order_item_id, "product_id": it.product_id.map(pid), "seller_id": it.seller_id.map(sid), "price": it.price, "freight": it.freight_value})
reviews = r.drop_duplicates("order_id").assign(order_id=lambda d: d.order_id.map(oid))[["order_id", "review_score", "review_creation_date"]].rename(columns={"review_score": "score", "review_creation_date": "created_at"})
reviews["has_comment"] = r.drop_duplicates("order_id").review_comment_message.notna().astype(int).values
tmap = dict(zip(tr.product_category_name, tr.product_category_name_english))
products = pd.DataFrame({"product_id": p.product_id.map(pid), "category": p.product_category_name.map(lambda x: tmap.get(x, x)).fillna("unknown"), "weight_g": p.product_weight_g, "photos": p.product_photos_qty})
sellers = pd.DataFrame({"seller_id": s.seller_id.map(sid), "state": s.seller_state})
payments = pd.DataFrame({"order_id": pay.order_id.map(oid), "type": pay.payment_type, "installments": pay.payment_installments, "value": pay.payment_value})
for col in ["purchased_at", "shipped_at", "delivered_at", "estimated_at"]:
    orders[col] = orders[col].str.slice(0, 10)
reviews["created_at"] = reviews["created_at"].str.slice(0, 10)
items["price"] = items.price.round(2); items["freight"] = items.freight.round(2); payments["value"] = payments.value.round(2)
os.makedirs("data", exist_ok=True)
if os.path.exists("data/olist.db"): os.remove("data/olist.db")
con = sqlite3.connect("data/olist.db")
for n, d in [("orders", orders), ("items", items), ("reviews", reviews), ("products", products), ("sellers", sellers)]:
    d.to_sql(n, con, index=False); print(n, len(d))
con.execute("VACUUM"); con.close()
with open("data/olist.db", "rb") as f, gzip.open("data/olist.db.gz", "wb", compresslevel=9) as g: shutil.copyfileobj(f, g)
os.remove("data/olist.db")
print("gz MB", round(os.path.getsize("data/olist.db.gz") / 1e6, 2))
